from django.conf import settings
from django.db import models
from django.utils import timezone
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

class GoogleDriveFile(models.Model):
    # Store metadata of the Google Drive file
    file_name = models.CharField(max_length=255)
    file_id = models.CharField(max_length=255)  # Google Drive file ID
    file_url = models.URLField()  # URL to access the file directly
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    # Link to a related model if necessary (e.g., Enquiry or other)
    enquiry = models.ForeignKey('Enquiry', on_delete=models.CASCADE, related_name="drive_files", null=True, blank=True)

    def __str__(self):
        return f"File: {self.file_name} ({self.file_id})"

    # Upload to Google Drive via API
    def upload_to_google_drive(self, file_path):
        """
        Uploads the given file to Google Drive and stores metadata in the model
        """
        # Authenticate using a service account
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/drive.file"]
        )
        
        # Build the Google Drive API client
        service = build('drive', 'v3', credentials=creds)

        # Prepare the file metadata
        file_metadata = {
            'name': self.file_name,
            'mimeType': 'application/octet-stream'  # Adjust mime type according to the file
        }

        # Read the file data
        media = MediaFileUpload(file_path, mimetype='application/octet-stream')

        # Upload the file to Google Drive
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        # Update the model with file ID and URL
        self.file_id = file.get('id')
        self.file_url = file.get('webViewLink')
        self.save()


class Enquiry(models.Model):
    SERVICE_CHOICES = [
        ('select_service', 'Select Service'),
        ('solar', 'Solar'),
        ('cctv', 'CCTV'),
        ('Network System and Networking', 'Network System and Networking'),
    ]
    
    PREMISES_CHOICES = [
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Retail Store', 'Retail Store'),
        ('Warehouse', 'Warehouse'),
        ('Factory', 'Factory'),
    ]
    
    # Basic Fields
    name = models.CharField(max_length=25)
    phone_number_1 = models.CharField(max_length=10)
    phone_number_2 = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Service Related
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    
    # Conditional Fields for Solar Service
    solar_budget = models.CharField(max_length=100, blank=True, null=True)

    # Conditional Fields for CCTV Service
    premises_type = models.CharField(max_length=50, choices=PREMISES_CHOICES, blank=True, null=True)
    num_cameras = models.IntegerField(blank=True, null=True)
    budget_range = models.CharField(max_length=50, blank=True, null=True)
    installation_address = models.TextField(blank=True, null=True)

    # Additional Comments for Solar and CCTV
    solar_comments = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)  # Correct timezone handling

    def __str__(self):
        return f"Enquiry for {self.name} - {self.service_type}"

    def save(self, *args, **kwargs):
        # Custom save method for handling file upload (if any)
        super().save(*args, **kwargs)  # First save the Enquiry instance
        
        if self.service_type == 'solar' or self.service_type == 'cctv':
            # Handle Google Drive upload logic for these services
            drive_file = GoogleDriveFile.objects.create(
                file_name=f"{self.name}_document.pdf",  # Example: Set a name for your file
                enquiry=self  # Associate with this enquiry
            )
            # Upload the file to Google Drive (for illustration purposes)
            drive_file.upload_to_google_drive('path/to/file.pdf')  # Replace with actual file path


# Other models
class Visitor(models.Model):
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Allow null values
    ip_address = models.GenericIPAddressField()
    visit_time = models.DateTimeField(default=timezone.now)  # Default to current time if not provided

    def __str__(self):
        return f"{self.email} - {self.ip_address} - {self.visit_time}"

class CCTVData(models.Model):
    date = models.DateField()  # Ensure there's a date field
    value = models.FloatField() 

    def __str__(self):
        return f"{self.date} - {self.value}"

class SolarData(models.Model):
    date = models.DateTimeField(default=timezone.now)  # Ensure this is a callable default
    value = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.date} - {self.value}"

class WhatsAppenquiry(models.Model):
    date = models.DateTimeField(default=timezone.now)  # Ensure this is a callable default
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.value}"
    
class Carousel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='carousel/')
    button_text = models.CharField(max_length=50, null=True, blank=True)
    button_link = models.URLField(null=True, blank=True)

class Feature(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # Store the FontAwesome class
    count = models.PositiveIntegerField()

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    link = models.URLField()

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Request(models.Model):
    CATEGORY_CHOICES = [
        ('CCTV', 'CCTV'),
        ('Solar', 'Solar'),
        ('WhatsApp', 'WhatsApp'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    request_date = models.DateTimeField(auto_now_add=True)  # Ensure the field name is request_date

    def __str__(self):
        return f'{self.category} request at {self.request_date}'

class contact_enquiry(models.Model):
    SERVICE_CHOICES = [
        ('solar', 'Solar'),
        ('cctv', 'CCTV'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, verbose_name="Full Name", default='')
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(max_length=254, verbose_name="Email Address", default='')
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_CHOICES,
        default='other',
        verbose_name="Service Type"
    )
    additional_comments = models.TextField(blank=True, verbose_name="Additional Comments", default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type.capitalize()}"
