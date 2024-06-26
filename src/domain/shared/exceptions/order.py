from src.domain.shared.exceptions.base import DomainException


class OrderNotFoundException(DomainException):
    def __init__(self, message="Order not found."):
        super().__init__(message)


class NoOrderFoundException(DomainException):
    def __init__(self, message="No order found."):
        super().__init__(message)


class InvalidOrderStatusException(DomainException):
    def __init__(self, message="Invalid order status."):
        super().__init__(message)


class OrderStatusProgressionNotAllowedException(DomainException):
    def __init__(self, message="Order status progression not allowed."):
        super().__init__(message)


class OrderItemInvalidQtyException(DomainException):
    def __init__(self, message="Order item quantity should be greater than zero."):
        super().__init__(message)
