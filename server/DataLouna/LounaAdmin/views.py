from django.shortcuts import render, redirect


def RedirectToAdmin(request):
    return redirect('/admin/')


