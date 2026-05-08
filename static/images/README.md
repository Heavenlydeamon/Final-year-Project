# Static Images Folder

This folder contains static image files for the EcoHeritage project.

## Usage

Place your images here to serve them as static files in Django templates:

```html
<img src="{% static 'images/your-image.png' %}" alt="Description">
```

## Image Types

- PNG, JPG, JPEG, GIF, SVG, WebP formats are supported
- Optimize images for web use before uploading
- Use descriptive filenames

## Organization

You can create subfolders to organize images by category:
- `images/logos/` - Logo files
- `images/icons/` - Icon files  
- `images/backgrounds/` - Background images
- `images/content/` - Content images
