import pytest
from unittest.mock import Mock, patch
from burger import Burger
from bun import Bun
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:

    def test_set_buns_should_set_bun(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        
        burger.set_buns(mock_bun)
        
        assert burger.bun == mock_bun #Проверка добавления булочки в бургер

    def test_add_ingredient_should_add_to_list(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient #Проверка добавления ингредиента в бургер

    @pytest.mark.parametrize('initial_count, index_to_remove', [
        (3, 0),  # Удаление первого элемента
        (3, 1),  # Удаление среднего элемента
        (3, 2),  # Удаление последнего элемента
    ])
    def test_remove_ingredient_should_remove_by_index(self, initial_count, index_to_remove):
        burger = Burger()
        for i in range(initial_count):
            burger.add_ingredient(Mock(spec=Ingredient))
        
        burger.remove_ingredient(index_to_remove)
        
        assert len(burger.ingredients) == initial_count - 1 #Удаления ингредиента по индексу

    @pytest.mark.parametrize('from_index, to_index, expected_order', [
        (0, 2, [1, 2, 0]),  # Перемещение первого в конец
        (2, 0, [2, 0, 1]),  # Перемещение последнего в начало
        (1, 1, [0, 1, 2]),  # Перемещение на тот же индекс
    ])
    def test_move_ingredient_should_reorder_ingredients(self, from_index, to_index, expected_order):
        burger = Burger()
        mock_ingredients = [Mock(spec=Ingredient) for _ in range(3)]
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        
        burger.move_ingredient(from_index, to_index)
        
        result_order = [burger.ingredients[i] for i in range(3)]
        expected_result = [mock_ingredients[i] for i in expected_order]
        assert result_order == expected_result #Перемещения ингредиента

    def test_get_price_should_return_total_price(self):
        burger = Burger()
       
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = 50.0
        
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient1.get_price.return_value = 30.0
        mock_ingredient2 = Mock(spec=Ingredient)
        mock_ingredient2.get_price.return_value = 40.0
        
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        
        expected_price = 170.0
        
        assert burger.get_price() == expected_price #Проверка расчета общей стоимости бургера

    def test_get_receipt_should_return_formatted_string(self):
        burger = Burger()
      
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "black bun"
        
        mock_sauce = Mock(spec=Ingredient)
        mock_sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_sauce.get_name.return_value = "hot sauce"
        
        mock_filling = Mock(spec=Ingredient)
        mock_filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_filling.get_name.return_value = "cutlet"
        
        mock_bun.get_price.return_value = 100.0
        mock_sauce.get_price.return_value = 50.0
        mock_filling.get_price.return_value = 75.0
        
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        
        expected_receipt = (
            "(==== black bun ====)\n"
            "= sauce hot sauce =\n"
            "= filling cutlet =\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 325.0"
        )
        
        assert burger.get_receipt() == expected_receipt #Проверка формирования чека

    def test_get_price_with_no_ingredients(self):
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = 75.0
        
        burger.set_buns(mock_bun)
        
        expected_price = 150.0
        
        assert burger.get_price() == expected_price #Проверка расчета цены без ингредиентов

    def test_remove_ingredient_from_empty_list_should_raise_error(self):
        burger = Burger()
        
        with pytest.raises(IndexError):
            burger.remove_ingredient(0) #Проверка, что удаление из пустого списка вызывает ошибку

    def test_move_ingredient_with_invalid_index_should_raise_error(self):
        burger = Burger()
        burger.add_ingredient(Mock(spec=Ingredient))
        
        with pytest.raises(IndexError):
            burger.move_ingredient(1, 0)  #Проверка, что перемещение с неверными индексами вызывает ошибку

    def test_get_receipt_without_bun_should_raise_error(self):
        burger = Burger()
        burger.add_ingredient(Mock(spec=Ingredient))
        
        with pytest.raises(AttributeError):
            burger.get_receipt() #Проверка, что получение чека без булочки вызывает ошибку

    def test_add_multiple_ingredients_should_maintain_order(self):
        burger = Burger()
        mock_ingredients = [Mock(spec=Ingredient) for _ in range(5)]
        
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        
        assert burger.ingredients == mock_ingredients #Проверка порядка добавления нескольких ингредиентов

    @pytest.mark.parametrize('bun_price, ingredient_prices, expected_price', [
        (100.0, [50.0, 30.0], 280.0),  # 100*2 + 50 + 30 = 280
        (200.0, [], 400.0),              # 200*2 = 400
        (150.0, [75.0, 25.0, 50.0], 450.0),  # 150*2 + 75 + 25 + 50 = 450
    ])
    def test_get_price_parameterized(self, bun_price, ingredient_prices, expected_price):
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        for price in ingredient_prices:
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
        
        assert burger.get_price() == expected_price #Расчет цены с разными комбинациями

    def test_get_receipt_calls_get_price(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "white bun"
        burger.set_buns(mock_bun)
        
        with patch.object(burger, 'get_price', return_value=500.0) as mock_get_price:
            receipt = burger.get_receipt()
            
            mock_get_price.assert_called_once()
            assert "Price: 500.0" in receipt