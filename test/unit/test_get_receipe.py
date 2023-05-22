import pytest
from unittest.mock import patch
from src.controllers.receipecontroller import ReceipeController
from src.static.diets import Diet

@pytest.fixture
def receipe_controller():
    controller = ReceipeController(items_dao=None)
    return controller


@pytest.fixture
def test_data():
    receipe = {'diets': ['vegetarian']}
    available_items = {}
    diet = Diet('vegetarian')
    return receipe, available_items, diet

@pytest.mark.unit
@patch('src.controllers.receipecontroller.calculate_readiness')
def test_receipe_not_available_readiness_above_0_1(mock_calculate_readiness, receipe_controller, test_data):
    receipe, available_items, diet = test_data
    receipe['diets'] = ['vegan']
    mock_calculate_readiness.return_value = 0.5  
    result = receipe_controller.get_receipe_readiness(receipe, available_items, diet)
    assert result is None
    
@pytest.mark.unit
@patch('src.controllers.receipecontroller.calculate_readiness')
def test_receipe_not_available_readiness_below_0_1(mock_calculate_readiness, receipe_controller, test_data):
    receipe, available_items, diet = test_data
    receipe['diets'] = ['vegan']
    mock_calculate_readiness.return_value = 0.05  # Mock the calculate_readiness function
    result = receipe_controller.get_receipe_readiness(receipe, available_items, diet)
    assert result is None

@pytest.mark.unit
@patch('src.controllers.receipecontroller.calculate_readiness')
def test_receipe_available_readiness_above_0_1(mock_calculate_readiness, receipe_controller, test_data):
    # Test case 3: receipe is available and readiness is above 0.1
    receipe, available_items, diet = test_data
    mock_calculate_readiness.return_value = 0.8  
    result = receipe_controller.get_receipe_readiness(receipe, available_items, diet)
    assert result == 0.8

@pytest.mark.unit
@patch('src.controllers.receipecontroller.calculate_readiness')
def test_receipe_available_readiness_below_0_1(mock_calculate_readiness, receipe_controller, test_data):
    receipe, available_items, diet = test_data
    mock_calculate_readiness.return_value = 0.05  
    result = receipe_controller.get_receipe_readiness(receipe, available_items, diet)
    assert result is None