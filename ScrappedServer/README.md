# `.onion` **Server**

To implement CRUD (Create, Read, Update, Delete) operations in Django for an `.onion` URL (i.e., a service hosted on the Tor network), you can follow the same principles as regular Django CRUD operations. The `.onion` domain doesn't require any special changes to your Django app itself. However, you'll need to ensure that your server is properly configured to handle the Tor service. Below is a basic guide to set up Django CRUD operations for a project accessible via a `.onion` URL:

### 1. **Configure Django Project**
Ensure your Django project is properly configured as usual for basic CRUD operations. You can create a model and views to handle these operations.

### Example Model (`models.py`)
```python
from django.db import models

class OnionService(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### Example Views (`views.py`)
For CRUD operations, you can use Django’s generic views to simplify the code:

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import OnionService
from .forms import OnionServiceForm

# Create
def onion_service_create(request):
    if request.method == "POST":
        form = OnionServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('onion_service_list')
    else:
        form = OnionServiceForm()
    return render(request, 'onion_service_form.html', {'form': form})

# Read (List and Detail)
def onion_service_list(request):
    services = OnionService.objects.all()
    return render(request, 'onion_service_list.html', {'services': services})

def onion_service_detail(request, pk):
    service = get_object_or_404(OnionService, pk=pk)
    return render(request, 'onion_service_detail.html', {'service': service})

# Update
def onion_service_update(request, pk):
    service = get_object_or_404(OnionService, pk=pk)
    if request.method == "POST":
        form = OnionServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('onion_service_detail', pk=service.pk)
    else:
        form = OnionServiceForm(instance=service)
    return render(request, 'onion_service_form.html', {'form': form})

# Delete
def onion_service_delete(request, pk):
    service = get_object_or_404(OnionService, pk=pk)
    if request.method == "POST":
        service.delete()
        return redirect('onion_service_list')
    return render(request, 'onion_service_confirm_delete.html', {'service': service})
```

### Example Form (`forms.py`)
```python
from django import forms
from .models import OnionService

class OnionServiceForm(forms.ModelForm):
    class Meta:
        model = OnionService
        fields = ['title', 'description']
```

### Example Templates
You can create HTML templates like `onion_service_form.html`, `onion_service_list.html`, and `onion_service_detail.html` to handle the frontend.

---

### 2. **Configure Tor Hidden Service**

To host your Django application on a `.onion` domain, you need to configure a Tor hidden service on your server.

#### Steps:
1. **Install Tor** on your server.
   ```bash
   sudo apt install tor
   ```
   
2. **Configure the hidden service** by editing the Tor configuration file (`/etc/tor/torrc`).

   Add the following lines to configure the hidden service:
   ```bash
   HiddenServiceDir /var/lib/tor/hidden_service/
   HiddenServicePort 80 127.0.0.1:8000  # This assumes your Django app runs on port 8000
   ```

3. **Restart Tor** to apply the changes:
   ```bash
   sudo service tor restart
   ```

4. **Get your .onion URL**. The hidden service's hostname (your `.onion` URL) will be generated and stored in the file:
   ```bash
   cat /var/lib/tor/hidden_service/hostname
   ```

   Use this URL to access your Django app via Tor.

---

### 3. **Adjust Security Settings**

To ensure your app can be accessed via `.onion` safely, you should make a few security-related adjustments in `settings.py`.

#### Example Settings:
- Allow the `.onion` domain in `ALLOWED_HOSTS`:
  ```python
  ALLOWED_HOSTS = ['your-onion-url.onion', '127.0.0.1']
  ```

- **Force HTTPS** (if necessary, depending on your setup with Tor):
  ```python
  SECURE_SSL_REDIRECT = True
  ```

- Make sure your server has the necessary security headers to protect against common web attacks.

---

### 4. **Accessing via the .onion Domain**
Once you’ve completed the above steps, your Django application should be accessible via the `.onion` URL. The CRUD operations will work just like in any normal Django app.

If you have further specific configurations or more details regarding your `.onion` service or the Tor network setup, feel free to ask!
