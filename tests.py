import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolioar.settings')

# Configure Django
django.setup()

# Now you can import models and other Django components
from django.test import TestCase
from core.models import User, Sector, Broker, Stock
from portfolio.models import Position, Order
from alerts.models import TechnicalIndicator, AlertCondition, Alert, AlertTrigger


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='testpass123',
            phone='1234567890',
            birthdate='1990-01-01'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, 'Juan')
        self.assertEqual(self.user.last_name, 'Pérez')
        self.assertEqual(self.user.email, 'juan@example.com')
        self.assertEqual(self.user.phone, '1234567890')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'Juan Pérez')


class SectorModelTest(TestCase):
    def setUp(self):
        self.sector = Sector.objects.create(
            name='Technology',
            description='Technology sector',
            primary=True
        )

    def test_sector_creation(self):
        self.assertEqual(self.sector.name, 'Technology')
        self.assertEqual(self.sector.description, 'Technology sector')
        self.assertTrue(self.sector.primary)

    def test_sector_str(self):
        self.assertEqual(str(self.sector), 'Technology')


class BrokerModelTest(TestCase):
    def setUp(self):
        self.broker = Broker.objects.create(
            name='IOL',
            link='https://invertironline.com'
        )

    def test_broker_creation(self):
        self.assertEqual(self.broker.name, 'IOL')
        self.assertEqual(self.broker.link, 'https://invertironline.com')

    def test_broker_str(self):
        self.assertEqual(str(self.broker), 'IOL')


class StockModelTest(TestCase):
    def setUp(self):
        self.sector = Sector.objects.create(name='Technology')
        self.stock = Stock.objects.create(
            ticker='AAPL',
            company_name='Apple Inc.',
            sector=self.sector
        )

    def test_stock_creation(self):
        self.assertEqual(self.stock.ticker, 'AAPL')
        self.assertEqual(self.stock.company_name, 'Apple Inc.')
        self.assertEqual(self.stock.sector, self.sector)

    def test_stock_str(self):
        self.assertEqual(str(self.stock), 'AAPL - Apple Inc.')


class PositionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='testpass123'
        )
        self.sector = Sector.objects.create(name='Technology')
        self.stock = Stock.objects.create(
            ticker='AAPL',
            company_name='Apple Inc.',
            sector=self.sector
        )
        self.broker = Broker.objects.create(name='IOL')
        self.position = Position.objects.create(
            user=self.user,
            stock=self.stock,
            broker=self.broker,
            amount=10,
            stock_price_local=15000.00,
            stock_price_usd=150.00,
            purchased_at='2024-01-01'
        )

    def test_position_creation(self):
        self.assertEqual(self.position.user, self.user)
        self.assertEqual(self.position.stock, self.stock)
        self.assertEqual(self.position.broker, self.broker)
        self.assertEqual(self.position.amount, 10)
        self.assertEqual(self.position.stock_price_local, 15000.00)
        self.assertEqual(self.position.stock_price_usd, 150.00)

    def test_position_str(self):
        self.assertEqual(str(self.position), 'AAPL - 10 unidades')


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='testpass123'
        )
        self.sector = Sector.objects.create(name='Technology')
        self.stock = Stock.objects.create(
            ticker='AAPL',
            company_name='Apple Inc.',
            sector=self.sector
        )
        self.broker = Broker.objects.create(name='IOL')
        self.position = Position.objects.create(
            user=self.user,
            stock=self.stock,
            broker=self.broker,
            amount=10,
            stock_price_local=15000.00,
            stock_price_usd=150.00,
            purchased_at='2024-01-01'
        )
        self.order = Order.objects.create(
            position=self.position,
            amount=5,
            fulfill_datetime='2024-01-15',
            total_fees=100.00,
            price_local=16000.00,
            price_usd=160.00
        )

    def test_order_creation(self):
        self.assertEqual(self.order.position, self.position)
        self.assertEqual(self.order.amount, 5)
        self.assertEqual(self.order.total_fees, 100.00)
        self.assertEqual(self.order.price_local, 16000.00)
        self.assertEqual(self.order.price_usd, 160.00)

    def test_order_str(self):
        self.assertEqual(str(self.order), f'Orden {self.order.id} - AAPL')


class TechnicalIndicatorModelTest(TestCase):
    def setUp(self):
        self.indicator = TechnicalIndicator.objects.create(
            name='RSI',
            description='Relative Strength Index',
            period=14
        )

    def test_indicator_creation(self):
        self.assertEqual(self.indicator.name, 'RSI')
        self.assertEqual(self.indicator.description, 'Relative Strength Index')
        self.assertEqual(self.indicator.period, 14)

    def test_indicator_str(self):
        self.assertEqual(str(self.indicator), 'RSI')


class AlertConditionModelTest(TestCase):
    def setUp(self):
        self.indicator = TechnicalIndicator.objects.create(
            name='RSI',
            description='Relative Strength Index',
            period=14
        )
        self.condition = AlertCondition.objects.create(
            indicator=self.indicator,
            operator='>',
            threshold_value=70
        )

    def test_condition_creation(self):
        self.assertEqual(self.condition.indicator, self.indicator)
        self.assertEqual(self.condition.operator, '>')
        self.assertEqual(self.condition.threshold_value, 70)

    def test_condition_str(self):
        self.assertEqual(str(self.condition), 'RSI > 70')


class AlertModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='testpass123'
        )
        self.sector = Sector.objects.create(name='Technology')
        self.stock = Stock.objects.create(
            ticker='AAPL',
            company_name='Apple Inc.',
            sector=self.sector
        )
        self.alert = Alert.objects.create(
            user=self.user,
            stock=self.stock,
            name='RSI Alert',
            is_active=True
        )

    def test_alert_creation(self):
        self.assertEqual(self.alert.user, self.user)
        self.assertEqual(self.alert.stock, self.stock)
        self.assertEqual(self.alert.name, 'RSI Alert')
        self.assertTrue(self.alert.is_active)

    def test_alert_str(self):
        self.assertEqual(str(self.alert), 'RSI Alert - AAPL')


class AlertTriggerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='testpass123'
        )
        self.sector = Sector.objects.create(name='Technology')
        self.stock = Stock.objects.create(
            ticker='AAPL',
            company_name='Apple Inc.',
            sector=self.sector
        )
        self.alert = Alert.objects.create(
            user=self.user,
            stock=self.stock,
            name='RSI Alert',
            is_active=True
        )
        self.trigger = AlertTrigger.objects.create(
            alert=self.alert,
            ai_recommendation='RSI is above 70, consider selling'
        )

    def test_trigger_creation(self):
        self.assertEqual(self.trigger.alert, self.alert)
        self.assertEqual(self.trigger.ai_recommendation, 'RSI is above 70, consider selling')

    def test_trigger_str(self):
        self.assertEqual(str(self.trigger), f'Trigger {self.trigger.id} - RSI Alert')


class PortfolioManagerTest(TestCase):
    def setUp(self):
        from portfolio.business import PortfolioManager
        self.portfolio_manager = PortfolioManager()
        
        self.user = User.objects.create_user(
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='testpass123'
        )
        self.sector = Sector.objects.create(name='Technology')
        self.stock = Stock.objects.create(
            ticker='AAPL',
            company_name='Apple Inc.',
            sector=self.sector
        )
        self.broker = Broker.objects.create(name='IOL')
        self.position = Position.objects.create(
            user=self.user,
            stock=self.stock,
            broker=self.broker,
            amount=10,
            stock_price_local=15000.00,
            stock_price_usd=150.00,
            purchased_at='2024-01-01'
        )

    def test_calculate_position_performance(self):
        performance = self.portfolio_manager.calculate_position_performance(self.position)
        
        self.assertIn('invested_amount', performance)
        self.assertIn('current_value', performance)
        self.assertIn('profit_loss', performance)
        self.assertIn('profit_loss_percentage', performance)
        self.assertIn('annualized_return', performance)
        self.assertIn('days_held', performance)

    def test_compare_with_sp500(self):
        comparison = self.portfolio_manager.compare_with_sp500(self.position)
        
        self.assertIn('sp500_return', comparison)
        self.assertIn('alpha', comparison)

    def test_compare_with_inflation(self):
        comparison = self.portfolio_manager.compare_with_inflation(self.position)
        
        self.assertIn('inflation', comparison)
        self.assertIn('real_return', comparison)

    def test_calculate_portfolio_summary(self):
        summary = self.portfolio_manager.calculate_portfolio_summary(self.user.id)
        
        self.assertIn('total_invested', summary)
        self.assertIn('total_current_value', summary)
        self.assertIn('profit_loss', summary)
        self.assertIn('profit_loss_percentage', summary)
        self.assertIn('position_count', summary)
        self.assertIn('sp500_return', summary)
        self.assertIn('alpha', summary)
        self.assertIn('inflation', summary)
        self.assertIn('real_return', summary)
        self.assertIn('sector_distribution', summary)

    def test_get_technical_indicators(self):
        indicators = self.portfolio_manager.get_technical_indicators(self.position)
        
        self.assertIn('rsi', indicators)
        self.assertIn('macd', indicators)
        self.assertIn('macd_signal', indicators)
        self.assertIn('macd_histogram', indicators)
        self.assertIn('sma_20', indicators)
        self.assertIn('sma_50', indicators)
        self.assertIn('ema_30', indicators)
        self.assertIn('volume_relative', indicators)
        self.assertIn('volatility', indicators)

    def test_add_position_validation(self):
        with self.assertRaises(ValueError):
            self.portfolio_manager.add_position(
                self.user.id, self.stock.id, self.broker.id, 0, 15000.00, 150.00, '2024-01-01'
            )

    def test_update_position_validation(self):
        with self.assertRaises(ValueError):
            self.portfolio_manager.update_position(self.position.id, -1, 15000.00, 150.00)


class AlertManagerTest(TestCase):
    def setUp(self):
        from alerts.business import AlertManager
        self.alert_manager = AlertManager()
        
        self.user = User.objects.create_user(
            first_name='Juan',
            last_name='Pérez',
            email='juan@example.com',
            password='testpass123'
        )
        self.sector = Sector.objects.create(name='Technology')
        self.stock = Stock.objects.create(
            ticker='AAPL',
            company_name='Apple Inc.',
            sector=self.sector
        )
        self.indicator = TechnicalIndicator.objects.create(
            name='RSI',
            description='Relative Strength Index',
            period=14
        )
        self.condition = AlertCondition.objects.create(
            indicator=self.indicator,
            operator='>',
            threshold_value=70
        )
        self.alert = Alert.objects.create(
            user=self.user,
            stock=self.stock,
            name='RSI Alert',
            is_active=True
        )

    def test_create_alert(self):
        alert = self.alert_manager.create_alert(
            self.user.id, self.stock.id, 'Test Alert', True
        )
        self.assertEqual(alert.name, 'Test Alert')
        self.assertTrue(alert.is_active)

    def test_create_alert_validation(self):
        with self.assertRaises(ValueError):
            self.alert_manager.create_alert(
                self.user.id, self.stock.id, '', True
            )

    def test_evaluate_alert(self):
        self.alert.conditions.add(self.condition)
        
        current_values = {'rsi': 75}
        result = self.alert_manager.evaluate_alert(self.alert, current_values)
        self.assertTrue(result)
        
        current_values = {'rsi': 65}
        result = self.alert_manager.evaluate_alert(self.alert, current_values)
        self.assertFalse(result)

    def test_get_user_alerts(self):
        alerts = self.alert_manager.get_user_alerts(self.user.id)
        self.assertEqual(alerts.count(), 1)
        self.assertEqual(alerts.first(), self.alert)