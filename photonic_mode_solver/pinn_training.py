"""
PINN Training Framework for Photonic Modes
========================================

Implementation of Physics-Informed Neural Network training for photonic mode solving.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt

class PINN(nn.Module):
    """Physics-Informed Neural Network for photonic mode solving."""
    
    def __init__(self, input_dim: int = 2, hidden_layers: List[int] = [64, 64, 64], 
                 output_dim: int = 1, device: str = 'cpu'):
        """
        Initialize PINN.
        
        Args:
            input_dim: Dimension of input coordinates (x,y)
            hidden_layers: List of hidden layer sizes
            output_dim: Dimension of output (field amplitude)
            device: Device to run training on ('cpu' or 'cuda')
        """
        super(PINN, self).__init__()
        self.device = device
        
        layers = []
        prev_dim = input_dim
        
        # Create hidden layers
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.Tanh())
            prev_dim = hidden_dim
            
        # Output layer
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
        
        # Initialize weights
        self._initialize_weights()
        
    def _initialize_weights(self):
        """Initialize network weights."""
        for m in self.network.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)
                
    def forward(self, x):
        """Forward pass through the network."""
        return self.network(x)
        
    def predict(self, x):
        """Predict field distribution."""
        self.eval()  # Set to evaluation mode
        with torch.no_grad():
            return self.forward(x)
            
    def train(self, structure, frequency, analytical_solution, 
              epochs: int = 1000, learning_rate: float = 0.001):
        """
        Train PINN using physics-informed loss function.
        
        Args:
            structure: Photonic structure
            frequency: Operating frequency
            analytical_solution: Known analytical solution
            epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
        """
        # Set to training mode
        self.train()
        
        # Setup optimizer
        optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        
        # Generate training data points
        train_points = self._generate_training_points(structure)
        
        # Convert to tensors
        x_train = torch.tensor(train_points, dtype=torch.float32, device=self.device)
        y_train = torch.tensor(analytical_solution, dtype=torch.float32, device=self.device)
        
        # Training loop
        losses = []
        for epoch in range(epochs):
            optimizer.zero_grad()
            
            # Forward pass
            predictions = self.forward(x_train)
            
            # Physics-informed loss (Helmholtz equation residual)
            loss = self._physics_informed_loss(predictions, x_train, structure, frequency)
            
            # Regularization loss (L2 penalty)
            reg_loss = self._regularization_loss()
            
            # Total loss
            total_loss = loss + reg_loss
            
            # Backward pass
            total_loss.backward()
            optimizer.step()
            
            losses.append(total_loss.item())
            
            # Print progress
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss.item():.6f}")
                
        return losses
        
    def _generate_training_points(self, structure):
        """Generate training points for the PINN."""
        # This would create a grid of points based on the structure
        # For a simple case, we create a regular grid
        if hasattr(structure, 'width') and hasattr(structure, 'height'):
            # Create meshgrid for rectangular structure
            x = np.linspace(-structure.width/2, structure.width/2, 50)
            y = np.linspace(-structure.height/2, structure.height/2, 50)
            X, Y = np.meshgrid(x, y)
            
            # Flatten and stack
            points = np.column_stack([X.ravel(), Y.ravel()])
            return points
        else:
            # Default: random points
            return np.random.rand(1000, 2) * 2 - 1  # Random points in [-1,1]
            
    def _physics_informed_loss(self, predictions, points, structure, frequency):
        """
        Calculate physics-informed loss based on Helmholtz equation.
        
        Args:
            predictions: Network predictions
            points: Input coordinates
            structure: Photonic structure
            frequency: Operating frequency
            
        Returns:
            Physics-informed loss value
        """
        # For photonic modes, we solve the Helmholtz equation:
        # (∇² + k²)ψ = 0
        # where k = ω/c = 2πf/c
        
        # Calculate gradients using automatic differentiation
        points.requires_grad_(True)
        
        # Forward pass to get predictions
        psi = self.forward(points)
        
        # Calculate gradient of psi
        grad_psi = torch.autograd.grad(psi.sum(), points, create_graph=True)[0]
        
        # Calculate Laplacian of psi
        laplacian = torch.zeros_like(psi)
        for i in range(points.shape[1]):
            grad_psi_i = grad_psi[:, i]
            laplacian += torch.autograd.grad(grad_psi_i.sum(), points, create_graph=True)[0][:, i]
            
        # Helmholtz residual (assuming k² = 1 for normalization)
        # In practice, this would use actual frequency-dependent k
        k_squared = 1.0
        helmholtz_residual = laplacian + k_squared * psi
        
        # Loss is mean squared error of Helmholtz equation residual
        return torch.mean(helmholtz_residual**2)
        
    def _regularization_loss(self):
        """Add regularization to prevent overfitting."""
        # L2 regularization on weights
        l2_reg = torch.tensor(0.0, device=self.device)
        for param in self.parameters():
            l2_reg += torch.norm(param)
        return 0.001 * l2_reg  # Small regularization coefficient


class PINNTrainer:
    """Trainer for PINN models with enhanced features."""
    
    def __init__(self, pinn_model: PINN):
        self.model = pinn_model
        
    def train_with_physics_loss(self, structure, frequency, 
                               analytical_solution: np.ndarray, 
                               epochs: int = 1000, 
                               learning_rate: float = 0.001,
                               validation_split: float = 0.2):
        """
        Train PINN with physics-informed loss function and validation.
        
        Args:
            structure: Photonic structure
            frequency: Operating frequency
            analytical_solution: Known analytical solution
            epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            validation_split: Fraction of data for validation
            
        Returns:
            Training history
        """
        # Split data
        total_points = len(analytical_solution)
        val_size = int(total_points * validation_split)
        
        # Shuffle data
        indices = np.random.permutation(total_points)
        train_indices = indices[val_size:]
        val_indices = indices[:val_size]
        
        # Create training and validation sets
        train_data = self._prepare_training_data(structure, train_indices)
        val_data = self._prepare_training_data(structure, val_indices)
        
        # Setup optimizer
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Training loop with validation
        train_losses = []
        val_losses = []
        
        for epoch in range(epochs):
            # Training step
            self.model.train()
            optimizer.zero_grad()
            
            # Forward pass on training data
            train_predictions = self.model.forward(train_data['points'])
            train_loss = self._calculate_loss(train_predictions, train_data['targets'])
            
            # Backward pass
            train_loss.backward()
            optimizer.step()
            
            # Validation step
            self.model.eval()
            with torch.no_grad():
                val_predictions = self.model.forward(val_data['points'])
                val_loss = self._calculate_loss(val_predictions, val_data['targets'])
            
            train_losses.append(train_loss.item())
            val_losses.append(val_loss.item())
            
            # Print progress
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Train Loss: {train_loss.item():.6f}, Val Loss: {val_loss.item():.6f}")
                
        return {
            'train_losses': train_losses,
            'val_losses': val_losses
        }
        
    def _prepare_training_data(self, structure, indices):
        """Prepare training data for the PINN."""
        # Generate points and targets
        points = self.model._generate_training_points(structure)
        targets = np.array([1.0] * len(points))  # Placeholder targets
        
        # Convert to tensors
        points_tensor = torch.tensor(points[indices], dtype=torch.float32)
        targets_tensor = torch.tensor(targets[indices], dtype=torch.float32)
        
        return {
            'points': points_tensor,
            'targets': targets_tensor
        }
        
    def _calculate_loss(self, predictions, targets):
        """Calculate loss for PINN training."""
        # Mean squared error between predictions and targets
        return torch.mean((predictions - targets)**2)
        
    def visualize_training(self, history):
        """Visualize training progress."""
        plt.figure(figsize=(10, 6))
        plt.plot(history['train_losses'], label='Training Loss')
        plt.plot(history['val_losses'], label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('PINN Training Progress')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def save_model(self, filepath):
        """Save trained model."""
        torch.save(self.model.state_dict(), filepath)
        
    def load_model(self, filepath):
        """Load trained model."""
        self.model.load_state_dict(torch.load(filepath))