from decimal import Decimal
from datetime import datetime, timedelta
import requests
from .data_access import (
    get_positions_by_user, get_position_by_id, create_position,
    update_position, delete_position, get_orders_by_position,
    create_order, delete_order
)


class ExternalAPIs:
    @staticmethod
    def get_indec_inflation(start_date, end_date):
        try:
            url = "https://apis.datos.gob.ar/series/api/series/"
            params = {
                'ids': '148.3_INIVELNAL_DICI_M_26',
                'format': 'json'
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    return Decimal(str(data['data'][0][1]))
            return Decimal('0')
        except Exception:
            return Decimal('0')

    @staticmethod
    def get_sp500_performance(start_date, end_date):
        try:
            return Decimal('10.5')
        except Exception:
            return Decimal('0')

    @staticmethod
    def get_current_price(ticker):
        try:
            return Decimal('150.00')
        except Exception:
            return None


class PortfolioManager:
    def __init__(self):
        self.external_apis = ExternalAPIs()

    def get_user_positions(self, user_id):
        return get_positions_by_user(user_id)

    def get_position(self, position_id):
        return get_position_by_id(position_id)

    def add_position(self, user_id, stock_id, broker_id, amount, stock_price_local, stock_price_usd, purchased_at):
        if amount <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if stock_price_local <= 0 or stock_price_usd <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        return create_position(user_id, stock_id, broker_id, amount, stock_price_local, stock_price_usd, purchased_at)

    def update_position(self, position_id, amount=None, stock_price_local=None, stock_price_usd=None):
        if amount is not None and amount <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if stock_price_local is not None and stock_price_local <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if stock_price_usd is not None and stock_price_usd <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        return update_position(position_id, amount, stock_price_local, stock_price_usd)

    def remove_position(self, position_id):
        delete_position(position_id)

    def calculate_position_performance(self, position):
        invested_amount = position.amount * position.stock_price_usd
        current_price_usd = position.stock_price_usd
        current_value = position.amount * current_price_usd

        profit_loss = current_value - invested_amount
        profit_loss_percentage = (profit_loss / invested_amount * 100) if invested_amount > 0 else Decimal('0')

        days_held = (datetime.now() - position.purchased_at).days if position.purchased_at else 0
        years_held = Decimal(str(days_held)) / Decimal('365')
        annualized_return = ((profit_loss_percentage / years_held) if years_held > 0 else Decimal('0'))

        return {
            'invested_amount': invested_amount,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': profit_loss_percentage,
            'annualized_return': annualized_return,
            'days_held': days_held
        }

    def compare_with_sp500(self, position):
        if not position.purchased_at:
            return {'sp500_return': Decimal('0'), 'alpha': Decimal('0')}

        sp500_return = self.external_apis.get_sp500_performance(
            position.purchased_at.date(),
            datetime.now().date()
        )

        performance = self.calculate_position_performance(position)
        alpha = performance['profit_loss_percentage'] - sp500_return

        return {
            'sp500_return': sp500_return,
            'alpha': alpha
        }

    def compare_with_inflation(self, position):
        if not position.purchased_at:
            return {'inflation': Decimal('0'), 'real_return': Decimal('0')}

        inflation = self.external_apis.get_indec_inflation(
            position.purchased_at.date(),
            datetime.now().date()
        )

        performance = self.calculate_position_performance(position)
        real_return = performance['profit_loss_percentage'] - inflation

        return {
            'inflation': inflation,
            'real_return': real_return
        }

    def calculate_portfolio_summary(self, user_id):
        positions = get_positions_by_user(user_id)

        total_invested = Decimal('0')
        total_current_value = Decimal('0')

        for position in positions:
            invested = position.amount * position.stock_price_local
            current = position.amount * position.stock_price_usd
            total_invested += invested
            total_current_value += current

        profit_loss = total_current_value - total_invested
        profit_loss_percentage = (profit_loss / total_invested * 100) if total_invested > 0 else Decimal('0')

        total_sp500_return = self.external_apis.get_sp500_performance(
            datetime.now().date() - timedelta(days=365),
            datetime.now().date()
        )
        alpha = profit_loss_percentage - total_sp500_return

        total_inflation = self.external_apis.get_indec_inflation(
            datetime.now().date() - timedelta(days=365),
            datetime.now().date()
        )
        real_return = profit_loss_percentage - total_inflation

        sector_distribution = {}
        for position in positions:
            sector = position.stock.sector.name if position.stock.sector else 'Sin sector'
            if sector not in sector_distribution:
                sector_distribution[sector] = Decimal('0')
            sector_distribution[sector] += position.amount * position.stock_price_usd

        return {
            'total_invested': total_invested,
            'total_current_value': total_current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': profit_loss_percentage,
            'position_count': len(positions),
            'sp500_return': total_sp500_return,
            'alpha': alpha,
            'inflation': total_inflation,
            'real_return': real_return,
            'sector_distribution': sector_distribution
        }

    def get_technical_indicators(self, position):
        return {
            'rsi': Decimal('65.5'),
            'macd': Decimal('2.35'),
            'macd_signal': Decimal('1.89'),
            'macd_histogram': Decimal('0.46'),
            'sma_20': position.stock_price_usd * Decimal('0.98'),
            'sma_50': position.stock_price_usd * Decimal('0.95'),
            'ema_30': position.stock_price_usd * Decimal('0.97'),
            'volume_relative': Decimal('1.2'),
            'volatility': Decimal('18.5')
        }


class OrderManager:
    def get_position_orders(self, position_id):
        return get_orders_by_position(position_id)

    def add_order(self, position_id, amount, fulfill_datetime, total_fees, price_local, price_usd):
        if amount <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if price_local <= 0 or price_usd <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        return create_order(position_id, amount, fulfill_datetime, total_fees, price_local, price_usd)

    def remove_order(self, order_id):
        delete_order(order_id)