import stripe
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from .models import Item, Order

logger = logging.getLogger(__name__)

# Настройка ключа Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def item_detail(request, item_id):
    """Страница товара с кнопкой покупки."""
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item.html', {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

@csrf_protect
@require_POST
def buy_item(request, item_id):
    """Создаёт PaymentIntent для оплаты одного товара."""
    item = get_object_or_404(Item, id=item_id)

    try:
        # Создаем PaymentIntent для товара
        payment_intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),  # Сумма в центах
            currency=item.currency,
            metadata={'item_id': item.id},
        )

        # Возвращаем clientSecret, который будет использоваться на клиенте
        return JsonResponse({
            'clientSecret': payment_intent.client_secret,
            'itemId': item.id
        })

    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=500)

    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

@csrf_protect
@require_POST
def buy_order(request, order_id):
    """Создает PaymentIntent для оплаты заказа (без использования Checkout Session)."""
    try:
        order = get_object_or_404(Order, id=order_id)

        # Рассчитываем итоговую сумму с учетом скидок и налогов
        total_price = order.total_price()

        # Создаем PaymentIntent для всего заказа
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),
            currency=order.currency,
            metadata={'order_id': order.id},
        )

        # Сохраняем payment_intent в заказе
        order.stripe_payment_intent = payment_intent.id
        order.save()

        # Возвращаем clientSecret для клиента
        return JsonResponse({
            'clientSecret': payment_intent.client_secret,
            'orderId': order.id
        })

    except stripe.error.StripeError as e:
        logger.error(f"Stripe Ошибка: {str(e)}")
        return JsonResponse({"error": f"Stripe error: {str(e)}"}, status=500)

    except Exception as e:
        logger.error(f"Ошибка сервера: {str(e)}")
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

@csrf_exempt
@require_POST
def confirm_payment(request):
    """Обрабатывает подтверждение платежа через Webhook."""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest("Invalid webhook")

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        order = Order.objects.filter(stripe_payment_intent=payment_intent["id"]).first()
        if order:
            order.is_paid = True
            order.save()
    return JsonResponse({"status": "success"})

@csrf_exempt
def create_payment_intent(request, order_id):
    try:
        # Получаем заказ из базы данных по order_id
        order = Order.objects.get(id=order_id)

        # Рассчитываем итоговую сумму с учетом скидок и налогов
        total_price = order.total_price()

        # Создаем PaymentIntent через Stripe API
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),
            currency=order.currency,
            metadata={'order_id': order.id},
        )

        # Возвращаем clientSecret, который будет использоваться на клиенте
        return JsonResponse({'clientSecret': payment_intent.client_secret})

    except Order.DoesNotExist:
        return JsonResponse({'error': 'Заказ не найден'}, status=404)
    except stripe.error.StripeError as e:
        return JsonResponse({'error': f'Ошибка Stripe: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Не удалось создать Payment Intent: {str(e)}'}, status=500)

def order_detail(request, order_id):
    """Страница заказа с кнопкой оплаты."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order.html', {'order': order, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

def payment_success(request):
    """Страница успешной оплаты."""
    return render(request, 'success.html')

def payment_cancel(request):
    """Страница отмены платежа."""
    return render(request, 'cancel.html')
