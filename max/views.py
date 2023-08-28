from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .models import withvehicle, withoutvehicle


# Home page where the user is redirected
class HomePageView(TemplateView):
    template_name = "security/index.html"

# People with vehicle registration
class WithVehicle(LoginRequiredMixin, TemplateView):
    template_name = 'security/with_vehicle.html'
    success_url = reverse_lazy('withvehicle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['withvehicles'] = withvehicle.objects.order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        # Retrieve the form data from the POST request
        id_number = request.POST['id_number']
        name = request.POST['name']
        vehicle_registration = request.POST['vehicle_registration']
        phone_number = request.POST['phone_number']
        company = request.POST['company']
        purpose = request.POST['purpose']
        idphoto_base64 = request.POST['idphoto']  # Get the base64-encoded front ID image data
        vehiclephoto_base64 = request.POST['vehiclephoto']  # Get the base64-encoded back ID image data

        # Perform form validation
        errors = {}

        if purpose == 'Other':
            other_purpose = request.POST['other_purpose']
            purpose = f'Other - {other_purpose}'

        # Decode the base64 image data and save it as a file
        idphoto = None
        vehiclephoto = None

        if idphoto_base64:
            format, imgstr = idphoto_base64.split(';base64,')
            ext = format.split('/')[-1]
            idphoto = ContentFile(base64.b64decode(imgstr), name=f"{name}_idv.{ext}")

        if vehiclephoto_base64:
            format, imgstr = vehiclephoto_base64.split(';base64,')
            ext = format.split('/')[-1]
            vehiclephoto = ContentFile(base64.b64decode(imgstr), name=f"{name}_vehicle.{ext}")

        try:
            # Create a new withvehicle object and save it to the database
            with_vehicle = withvehicle.objects.create(
                id_number=id_number,
                name=name,
                vehicle_registration=vehicle_registration,
                phone_number=phone_number,
                company=company,
                purpose=purpose,
                time_in=timezone.localtime().time(),
                idphoto=idphoto,
                vehiclephoto=vehiclephoto
            )

            # Notify the user about successful submission
            messages.success(request, 'With Vehicle submitted successfully.')

            # Redirect to the home page
            return redirect('home')
        except Exception as e:
            # Notify the user about the error
            messages.error(request, f'Error: {str(e)}')

            # Redirect back to the form page
            return redirect('withvehicle')


# People without vehicle registration
from django.core.files.base import ContentFile
import base64

# ...

class WithoutVehicle(LoginRequiredMixin, TemplateView):
    template_name = 'security/without_vehicle.html'
    success_url = reverse_lazy('withoutvehicle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['withoutvehicles'] = withoutvehicle.objects.order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        # Retrieve the form data from the POST request
        id_number = request.POST['id_number']
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        company = request.POST['company']
        purpose = request.POST['purpose']
        idphoto_base64 = request.POST['idphoto']  # Get the base64-encoded front image data
        
        # Perform form validation
        errors = {}

        if purpose == 'Other':
            other_purpose = request.POST['other_purpose']
            purpose = f'Other - {other_purpose}'

        if not idphoto_base64:
            errors['idphoto'] = 'Please capture the front ID picture.'

        # Decode the base64 image data and save it as a file
        if idphoto_base64:
            format, imgstr = idphoto_base64.split(';base64,')  # Extract the format and base64 data
            ext = format.split('/')[-1]  # Extract the file extension
            idphoto = ContentFile(base64.b64decode(imgstr), name=f"{name}_front.{ext}")  # Create a ContentFile with decoded data
        else:
            idphoto = None

        # ...

        try:
            # Create a new withoutvehicle object and save it to the database
            without_vehicle = withoutvehicle.objects.create(
                id_number=id_number,
                name=name,
                phone_number=phone_number,
                company=company,
                purpose=purpose,
                time_in=timezone.localtime().time(),
                idphoto=idphoto,
            )

            # Notify the user about successful submission
            messages.success(request, 'Without Vehicle submitted successfully.')

            # Redirect to the success URL
            return redirect('home')
        except Exception as e:
            # Notify the user about the error
            messages.error(request, f'Error: {str(e)}')

            # Redirect back to the form page
            return redirect('withoutvehicle')


# For updating time for people with vehicles
from datetime import datetime, timedelta

class UpdateWithVehicleTimeOutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        withvehicle_id = kwargs['withvehicle_id']
        with_vehicle = withvehicle.objects.get(id=withvehicle_id)
        
        current_time = timezone.localtime()
        with_vehicle.time_out = current_time.time()

        time_in_datetime = datetime.combine(datetime.today(), with_vehicle.time_in)
        time_out_datetime = datetime.combine(datetime.today(), with_vehicle.time_out)

        time_difference = time_out_datetime - time_in_datetime
        hours = time_difference.seconds // 3600  # Calculate hours
        minutes = (time_difference.seconds // 60) % 60  # Calculate remaining minutes

        time_spent_timedelta = timedelta(hours=hours, minutes=minutes)

        with_vehicle.time_spent = time_spent_timedelta
        with_vehicle.Exit = True
        with_vehicle.save()

        if with_vehicle.time_out is not None:
            # Time updated successfully
            messages.success(request, 'Time Out WithVehicle Updated successfully.')
        else:
            # Failed to update time
            messages.error(request, 'Failed to update time.')

        return redirect('home')


# For updating time for people without vehicles

class UpdateWithoutVehicleTimeOutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        withoutvehicle_id = kwargs['withoutvehicle_id']
        without_vehicle = withoutvehicle.objects.get(id=withoutvehicle_id)
        
        current_time = timezone.localtime()
        without_vehicle.time_out = current_time.time()

        time_in_datetime = datetime.combine(datetime.today(), without_vehicle.time_in)
        time_out_datetime = datetime.combine(datetime.today(), without_vehicle.time_out)

        time_difference = time_out_datetime - time_in_datetime
        total_seconds = time_difference.total_seconds()
        hours = int(total_seconds // 3600)  # Calculate hours
        minutes = int((total_seconds // 60) % 60)  # Calculate remaining minutes

        without_vehicle.duration_hours = hours  # Store hours in the model
        without_vehicle.duration_minutes = minutes  # Store minutes in the model

        without_vehicle.time_spent = f'{hours}:{minutes:02}'  # Format hours and minutes
        without_vehicle.Exit = True
        without_vehicle.save()

        if without_vehicle.time_out is not None:
            # Time updated successfully
            messages.success(request, 'Time Out WithoutVehicle Updated successfully.')
        else:
            # Failed to update time
            messages.error(request, 'Failed to update time.')

        return redirect('home')




# For handling errors
from django.shortcuts import render

def handler404(request, exception):
    return render(request, 'security/404.html')


class ExitWithoutVehicle(LoginRequiredMixin, TemplateView):
    template_name = "security/exit_withoutvehicle.html"
    success_url = reverse_lazy("ExitWithoutVehicle")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['withoutvehicles'] = withoutvehicle.objects.order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        # Retrieve the form data from the POST request
        id_number = request.POST.get('id_number')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        company = request.POST.get('company')
        purpose = request.POST.get('purpose')
        

        # Retrieve the file from the request
        idphoto = request.FILES.get('idphoto')
   


        # Create a new WithoutVehicle object and save it to the database
        without_vehicle = withoutvehicle.objects.create(
            id_number=id_number,
            name=name,
            phone_number=phone_number,
            company=company,
            purpose=purpose,
            idphoto=idphoto, 
            time_in=timezone.localtime().time(),
             # Associate the file with the attribute
            
        )

        # Update the context with the submitted data
        self.extra_context = {'submitted_data': without_vehicle}

        # Redirect to the success URL
        return redirect('ExitWithoutVehicle')

# Exit with vehicle registration
class ExitWithVehicle(LoginRequiredMixin, TemplateView):
    template_name = "security/exit_withvehicle.html"
    success_url = reverse_lazy('ExitWithVehicle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['withvehicles'] = withvehicle.objects.order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        # Retrieve the form data from the POST request
        id_number = request.POST['id_number']
        name = request.POST['name']
        vehicle_registration = request.POST['vehicle_registration']
        phone_number = request.POST['phone_number']
        company = request.POST['company']
        purpose = request.POST['purpose']
        idphoto = request.FILES.get('idphoto')
        vehiclephoto=request.FILES.get('vehiclephoto')
        

        try:
            time_in = timezone.localtime()
            time_out = timezone.localtime()
            

            # Create a new withvehicle object and save it to the database
            with_vehicle = withvehicle.objects.create(
                id_number=id_number,
                name=name,
                vehicle_registration=vehicle_registration,
                phone_number=phone_number,
                company=company,
                purpose=purpose,
                idphoto=idphoto,
                vehiclephoto=vehiclephoto,
                time_in=time_in,
                time_out=time_out,
               
                
            )

            # Add a success flash message
            messages.add_message(request, messages.SUCCESS, 'WithVehicle saved successfully.')

        except Exception as e: 
            # Add an error flash message
            messages.add_message(request, messages.ERROR, f'Error: {str(e)}')

        # Redirect to the success URL
        return redirect('home')
#views for calulating the time spent 





