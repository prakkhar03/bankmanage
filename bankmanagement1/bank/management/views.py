from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import UserProfile, Transaction
import random
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('mainpage')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        data = request.POST
        n = data.get("name")
        an = data.get('aadhar_number')
        pn = data.get('phone_number')
        dob = data.get('date_of_birth')
        add = data.get('address')
        passw = data.get('password')
        b = 0
        c = True
        while c:
            account_no = random.randint(1000000000, 9999999999)
            if not UserProfile.objects.filter(account_number=account_no).exists():
                c = False
                user = User.objects.create_user(
                    username=str(account_no),
                    password=passw,
                    first_name=n
                )
                user_profile = UserProfile.objects.create(
                    user=user,
                    aadhar_number=an,
                    phone_number=pn,
                    date_of_birth=dob,
                    address=add,
                    balance=b,
                    account_number=account_no
                )
                messages.success(request, f'Account created successfully! Your account number is {account_no}')
                return redirect('login')

    return render(request, "register.html")
@login_required
def deposit(request):
    if request.method == 'POST':
        data = request.POST
        accno = data.get("accountNumber")
        amount = data.get("amount")

        try:
            user_profile = UserProfile.objects.get(account_number=accno)
            deposit_amount = float(amount)

            if deposit_amount <= 0:
                raise ValueError("Deposit amount must be positive.")

            user_profile.balance += Decimal(deposit_amount)
            user_profile.save()

            Transaction.objects.create(
                user_profile=user_profile,
                transaction_type='deposit',
                amount=deposit_amount,
                description='Deposit to account'
            )

            messages.success(request, "Deposit successful!")
            return redirect('balance')

        except UserProfile.DoesNotExist:
            messages.error(request, "Account not found.")
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'deposite.html')
@login_required
def withdrawal(request):
    if request.method == 'POST':
        data = request.POST
        accno = data.get("accountNumber")
        amt = data.get("amount")

        try:
            user_profile = UserProfile.objects.get(account_number=accno)
            withdraw_amount = float(amt)

            if withdraw_amount <= 0:
                raise ValueError("Withdrawal amount must be positive.")
            if user_profile.balance < withdraw_amount:
                raise ValueError("Insufficient balance.")

            user_profile.balance -= Decimal(withdraw_amount)
            user_profile.save()

            Transaction.objects.create(
                user_profile=user_profile,
                transaction_type='withdrawal',
                amount=withdraw_amount,
                description='Withdrawal from account'
            )

            messages.success(request, "Withdrawal successful!")
            return redirect('balance')

        except UserProfile.DoesNotExist:
            messages.error(request, "Account not found.")
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'withdrawl.html')
@login_required
def balance(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'balance.html', {'balance': user_profile.balance})
@login_required
def transfer(request):
    if request.method == 'POST':
        sender_accno = request.POST.get("senderAccountNumber")
        receiver_accno = request.POST.get("receiverAccountNumber")
        amount = request.POST.get("amount")

        try:
            sender_profile = UserProfile.objects.get(account_number=sender_accno)
            receiver_profile = UserProfile.objects.get(account_number=receiver_accno)
            transfer_amount = float(amount)

            if transfer_amount <= 0:
                raise ValueError("Transfer amount must be positive.")
            if sender_profile.balance < transfer_amount:
                raise ValueError("Insufficient balance.")

            sender_profile.balance -= transfer_amount
            receiver_profile.balance += transfer_amount
            sender_profile.save()
            receiver_profile.save()
            
            Transaction.objects.create(
                user_profile=sender_profile,
                transaction_type='transfer',
                amount=transfer_amount,
                description=f'Transfer to {receiver_accno}'
            )
            Transaction.objects.create(
                user_profile=receiver_profile,
                transaction_type='transfer',
                amount=transfer_amount,
                description=f'Transfer from {sender_accno}'
            )

            messages.success(request, "Transfer successful!")
            return redirect('balance')

        except UserProfile.DoesNotExist:
            messages.error(request, "Account not found.")
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'transfer.html')

@login_required
def history(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    transactions = Transaction.objects.filter(user_profile=user_profile).order_by('-timestamp')
    return render(request, 'history.html', {'transactions': transactions})
@login_required
def mainpage(request):
    return render(request, 'mainpage.html')

def exit(request):
    return render(request, 'login.html')
