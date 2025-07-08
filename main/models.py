from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    """User profile settings specific to the website"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    institution = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.institution}"

class Researcher(models.Model):
    """Researcher profiles in the community"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    photo = models.ImageField(upload_to='researcher_photos/', blank=True)
    research_areas = models.TextField(help_text="Comma-separated research areas")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.institution}"

class Reference(models.Model):
    """Database of papers and books"""
    REFERENCE_TYPES = [
        ('paper', 'Paper'),
        ('book', 'Book'),
        ('thesis', 'Thesis'),
        ('preprint', 'Preprint'),
        ('article', 'Article'),
    ]
    
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=1000)
    year = models.IntegerField()
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPES)
    journal = models.CharField(max_length=200, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to='references/', blank=True)
    abstract = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    added_by = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.year})"

class Project(models.Model):
    """Collaborative research projects"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    lead_researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE, related_name='led_projects')
    collaborators = models.ManyToManyField(Researcher, related_name='collaborating_projects', blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ], default='active')
    website = models.URLField(blank=True)
    repository = models.URLField(blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    """Events and conferences"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    venue = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    registration_url = models.URLField(blank=True)
    organizers = models.ManyToManyField(Researcher, related_name='organized_events', blank=True)
    speakers = models.ManyToManyField(Researcher, related_name='speaking_events', blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%Y-%m-%d')}"

class Post(models.Model):
    """Blog posts by researchers"""
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='post_images/', blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    related_projects = models.ManyToManyField(Project, blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

# Additional models for event management
class Talk(models.Model):
    """Talks within events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='talks')
    title = models.CharField(max_length=300)
    speaker = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    abstract = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    slides = models.FileField(upload_to='talk_slides/', blank=True)
    video_url = models.URLField(blank=True)
    room = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.title} - {self.speaker.name}"

class Organizer(models.Model):
    """Event organizers (can be researchers or external)"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_organizers')
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    institution = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Speaker(models.Model):
    """Event speakers"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_speakers')
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='speaker_photos/', blank=True)
    institution = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
