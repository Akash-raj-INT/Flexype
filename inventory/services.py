from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Inventory, Reservation

RESERVATION_TTL = 5

@transaction.atomic
def reserve_item(sku):
    inventory = Inventory.objects.select_for_update().get(sku=sku)

    active = Reservation.objects.filter(
        inventory=inventory,
        status='ACTIVE',
        expires_at__gt=timezone.now()
    ).count()

    if active >= inventory.total_stock:
        return None

    return Reservation.objects.create(
        inventory=inventory,
        expires_at=timezone.now() + timedelta(minutes=RESERVATION_TTL)
    )
@transaction.atomic
def confirm_reservation(reservation_id):
    if not reservation_id:
        return False

    try:
        reservation = Reservation.objects.select_for_update().get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    if reservation.status != 'ACTIVE':
        return False

    if reservation.expires_at < timezone.now():
        reservation.status = 'EXPIRED'
        reservation.save()
        return False

    reservation.status = 'CONFIRMED'
    reservation.save()
    return True


@transaction.atomic
def cancel_reservation(reservation_id):
    try:
        reservation = Reservation.objects.select_for_update().get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    if reservation.status == 'ACTIVE':
        reservation.status = 'CANCELLED'
        reservation.save()
    return True

def get_inventory_status(sku):
    try:
        inventory = Inventory.objects.get(sku=sku)
    except Inventory.DoesNotExist:
        return None

    active_reservations = Reservation.objects.filter(
        inventory=inventory,
        status='ACTIVE',
        expires_at__gt=timezone.now()
    ).count()

    available_stock = inventory.total_stock - active_reservations

    return {
        "sku": inventory.sku,
        "total_stock": inventory.total_stock,
        "available_stock": max(available_stock, 0)
    }