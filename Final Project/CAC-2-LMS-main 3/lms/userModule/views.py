from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Usertbl, Orderstbl, Payment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse


def index(request):
    return render(request, "userM/home.html")


def signup_login(request):
    return render(request, "userM/signup-login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        usertype = request.POST['usertype']

        if not User.objects.filter(username=username).exists():
            if pass1 == pass2:

                myuser = User.objects.create_user(username, email, pass1)
                if usertype == "staff":
                    myuser.is_staff = True
                myuser.save()

                user_tbl = Usertbl(
                    user=myuser,
                    usertype=usertype,
                    username=username,
                    useremail=email,

                )
                user_tbl.save()
                return render(request, "userM/signup-login.html", {'success_message': "User got Created"})
            else:
                return render(request, "userM/signup-login.html",
                              {'password_error_message': "Check your conformation password"})
        else:
            return render(request, "userM/signup-login.html", {'username_error_message': "Username Already Exist"})

    return render(request, "userM/signup-login.html")


# def signup(request):
#     if request.method == 'POST':
#         Userregnoid = request.POST.get('regnoid')
#         Username = request.POST.get('name')
#         Password = request.POST.get('password')
#         Useremail = request.POST.get('email')
#         Usertype = request.POST.get('userType')

#         # Check if a user with the given email already exists
#         if User.objects.filter(email=Useremail).exists():
#             messages.error(request, "User with this email already exists.")
#             return redirect('signup')

#         is_staff = (Usertype == 'staff')

#         # Create a new user using Django's User model
#         my_user = User.objects.create_user(username=Username, email=Useremail, password=Password)

#         # Save the user profile information in your custom model
#         user_profile = Usertbl(
#             username=Username,
#             useremail=Useremail,
#             userRegnoID=Userregnoid,
#             is_staff=is_staff
#         )
#         user_profile.save()

#         print("User profile insertion started")
#         print(f"Is_staff: {is_staff}")

#         return redirect('login')
#     else:
#         return render(request, "userM/signup-login.html")  # Signup 
# def login(request):
#     if request.method == 'POST':
#         Useremail = request.POST.get('email')
#         Password = request.POST.get('password')
#         Usertype = request.POST.get('userType')

#         user = authenticate(request, useremail = Useremail, password = Password )

#         if user is not None:
#             user_profile = user.userprofile

#             if Usertype == 'user' and not user_profile.is_staff:
#                 login(request, user)
#                 return redirect('index')
#             elif Usertype == 'host' and user_profile.is_staff:
#                 login(request, user)
#                 return redirect('host')
#             else:
#                 messages.error(request, f"No {Usertype.capitalize()} account found with this email.")
#         else:
#             messages.error(request, "Invalid email or password.")

#     return render(request,"userM/signup-login.html") 


def user_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['password']
        user_type = request.POST['userType']

        # Perform authentication
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            if user.usertbl.is_admin:
                # Redirect to admin dashboard for admin users
                return redirect('dashboard')
            elif not user.is_staff:
                return redirect('user-w')  # Redirect to your home page or any desired URL after login
            elif user.is_staff:
                return redirect('staff_page')
        else:
            return render(request,'userM/loginerror.html')
            # Redirect back to the login page in case of authentication failure
    else:
        return render(request, "userM/signup-login.html")


def loginerror(request):
    return render(request, "userM/loginerror.html")


@login_required(login_url='user_login')
def userwelcome(request):
    return render(request, "userM/userwellcome.html")


@login_required(login_url='user_login')
def requestorder(request):
    if request.method == 'POST':
        # Extract form data from the request
        name = request.POST.get('Name')
        reg_no = request.POST.get('RegNo')
        department = request.POST.get('Department')
        service_type = request.POST.get('Service')
        quantity = request.POST.get('Quantity')
        amount = request.POST.get('Amount')
        expected_delivery_date = request.POST.get('Delivery')

        # Perform basic form validation (you can add more checks)
        if not name or not reg_no or not department or not service_type or not quantity or not amount or not expected_delivery_date:
            return HttpResponse("All fields are required.")

        # Convert lazy-loaded user to Usertbl instance
        user_instance = User.objects.get(username=request.user.username).usertbl

        # Create an Orderstbl instance and save it to the database
        order = Orderstbl(
            user=user_instance,
            service_type=service_type,
            quantity=quantity,
            amount=amount,
            expected_delivery_date=expected_delivery_date,
            payment_completed=False
        )
        order.save()

        # Redirect to a success page or home page
        return redirect('payment', order_id=order.id)  # Replace 'home' with the actual URL name of your home page

    return render(request, "userM/request.html")


@login_required(login_url='user_login')
def payment(request, order_id):
    order = get_object_or_404(Orderstbl, id=order_id)

    if request.method == 'POST':
        amount_paid_str = request.POST.get('amount_paid', '0')
        try:
            amount_paid = Decimal(amount_paid_str)
        except DecimalException:
            amount_paid = Decimal(0)

        due_amount = max(order.amount - amount_paid, 0)

        order.payment_completed = amount_paid >= order.amount
        order.save()

        payment = Payment(order=order, amount_paid=amount_paid, due_amount=due_amount,
                          payment_status='SUCCESS' if order.payment_completed else 'PENDING')
        payment.save()

        context = {
            'order': order,
            'amount_paid': amount_paid,
            'due_amount': due_amount,
            'user_name': order.user.username,
            'tracking_id': order.id,
        }

        return render(request, 'userM/requestdone.html', context)

    return render(request, "userM/payment.html", {'order': order})


@login_required(login_url='user_login')
def requestdone(request):
    return render(request, "userM/requestdone.html")


@login_required(login_url='user_login')
def trackstatus(request):
    if request.method == 'POST':
        tracking_id = request.POST.get('TrackingId')

        # Query the database to get the order with the provided Tracking ID
        order = get_object_or_404(Orderstbl, id=tracking_id)

        # Pass the order information to the template context
        context = {
            'order': order,
            # 'status': order.status  # Replace 'status' with the actual field name in your Orderstbl model
        }

        return render(request, 'userM/showstatus.html', context)

    return render(request, 'userM/trackstatus.html')


@login_required(login_url='user_login')
def showstatus(request):
    return render(request, "userM/showstatus.html")


@login_required(login_url='user_login')
def signout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='user_login')
def dashboard(request):
    # Fetch recent orders from the database
    recent_orders = Orderstbl.objects.all().order_by('-id')[:5]
    comp = Complaint.objects.all()

    # Assuming you want to display the 5 most recent orders

    context = {
        'recent_orders': recent_orders,
        'complaints': comp,

    }

    return render(request, "userM/dashboard.html", context)


def invoice(request, order_id):
    order = Orderstbl.objects.get(pk=order_id)
    user = order.user
    payment = Payment.objects.filter(order=order).first()  # Assuming there's only one payment per order

    context = {
        'order': order,
        'user': user,
        'payment': payment,
    }
    return render(request, 'userM/invoice.html', context)


@login_required(login_url='user_login')
def staff_page(request):
    # Fetch orders along with their related Payment objects
    orders = Orderstbl.objects.prefetch_related('payment_set').all()

    context = {
        'orders': orders,
    }

    return render(request, "userM/staff_page.html", context)


def order_details(request, order_id):
    order = get_object_or_404(Orderstbl, id=order_id)
    # Render order details template with order data
    return render(request, 'userM/order_details.html', {'order': order})


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = Orderstbl.objects.get(id=order_id)
        status = request.POST.get('status')

        if status == 'completed':
            order.delivery_status = 'Washing Completed'
        elif status == 'delivered':
            order.delivery_status = 'Delivered on Time'
        elif status == 'received':
            order.delivery_status = 'User Received Clothes'

        order.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'success': False})


def view_details(request, order_id):
    # Fetch the order details from the database
    order = Orderstbl.objects.get(pk=order_id)
    user = order.user
    payment = Payment.objects.filter(order=order).first()  # Assuming there's only one payment per order

    context = {
        'order': order,
        'user': user,
        'payment': payment,
    }
    # Pass the order details to the template
    return render(request, 'userM/view_details.html', context)
