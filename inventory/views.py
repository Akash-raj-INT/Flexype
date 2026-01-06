from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import reserve_item
from .services import confirm_reservation
from .services import cancel_reservation
from .services import get_inventory_status


class ReserveInventoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sku = request.data.get("sku")
        reservation = reserve_item(sku)

        if not reservation:
            return Response({"error": "Out of stock"}, status=400)

        return Response({
            "reservation_id": reservation.id,
            "expires_at": reservation.expires_at
        })

class ConfirmCheckoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reservation_id = request.data.get("reservation_id")

        if not reservation_id:
            return Response(
                {"error": "reservation_id is required"},
                status=400
            )

        success = confirm_reservation(reservation_id)

        if not success:
            return Response(
                {"error": "Invalid or expired reservation"},
                status=400
            )

        return Response({"status": "confirmed"})



class CancelCheckoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reservation_id = request.data.get("reservation_id")
        cancel_reservation(reservation_id)
        return Response({"status": "cancelled"})

class InventoryStatusAPI(APIView):
    def get(self, request, sku):
        data = get_inventory_status(sku)

        if not data:
            return Response(
                {"error": "SKU not found"},
                status=404
            )

        return Response(data)

