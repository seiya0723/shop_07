from shop.models import Cart

class AddNumAttribute:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.num = Cart.objects.filter(user=request.user.id).count()
        response = self.get_response(request)

        return response