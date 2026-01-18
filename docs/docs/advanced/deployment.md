# Deployment Guide

Learn how to deploy your Muwanx applications to various hosting services.

## Overview

Muwanx applications are static websites that can be deployed to any static hosting service. This guide covers popular deployment options.

## GitHub Pages

Perfect for open-source projects and demos.

### Setup

1. **Configure Base Path**

```python
# For user/org pages: https://username.github.io/
builder = mwx.Builder(base_path="/")

# For project pages: https://username.github.io/repo-name/
builder = mwx.Builder(base_path="/repo-name/")
```

2. **Build to Docs Folder**

```python
app = builder.build(output_dir="./docs")
```

3. **Configure Repository**

- Go to repository Settings → Pages
- Source: Deploy from a branch
- Branch: `main` (or your default branch)
- Folder: `/docs`
- Save

4. **Push and Deploy**

```bash
git add docs/
git commit -m "Deploy Muwanx app"
git push
```

Your site will be available at `https://username.github.io/repo-name/`

### GitHub Actions (Automated)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install muwanx

      - name: Build application
        run: python build.py

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

## Netlify

Great for automatic deployments with preview branches.

### Method 1: Drag and Drop

1. Build your application:

```python
app = builder.build(output_dir="./dist")
```

2. Go to [Netlify](https://netlify.com)
3. Drag the `dist` folder to deploy

### Method 2: Git Integration

1. Create `netlify.toml`:

```toml
[build]
  command = "pip install muwanx && python build.py"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. Create `requirements.txt`:

```
muwanx>=0.0.5
```

3. Connect repository in Netlify dashboard

4. Configure build settings:
   - Build command: (leave empty, using netlify.toml)
   - Publish directory: `dist`

### Method 3: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
python build.py

# Deploy
netlify deploy --prod --dir=dist
```

## Vercel

Fast deployment with excellent performance.

### Method 1: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Build
python build.py

# Deploy
vercel --prod
```

### Method 2: Git Integration

1. Create `vercel.json`:

```json
{
  "buildCommand": "pip install muwanx && python build.py",
  "outputDirectory": "dist"
}
```

2. Connect repository in Vercel dashboard

## AWS S3 + CloudFront

Enterprise-grade hosting with CDN.

### Setup S3 Bucket

```bash
# Create bucket
aws s3 mb s3://my-muwanx-app

# Configure for static hosting
aws s3 website s3://my-muwanx-app \
  --index-document index.html
```

### Deploy

```bash
# Build
python build.py

# Upload
aws s3 sync dist/ s3://my-muwanx-app/ \
  --acl public-read \
  --delete
```

### CloudFront CDN

1. Create CloudFront distribution pointing to S3 bucket
2. Configure HTTPS certificate
3. Set index document to `index.html`
4. Configure error pages to redirect to `index.html`

### Automated with GitHub Actions

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install muwanx

      - name: Build
        run: python build.py

      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://my-muwanx-app/ \
            --acl public-read \
            --delete

      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CF_DISTRIBUTION_ID }} \
            --paths "/*"
```

## Azure Static Web Apps

Microsoft's static hosting solution.

### Deploy with CLI

```bash
# Install Azure CLI
az extension add --name staticwebapp

# Build
python build.py

# Deploy
az staticwebapp create \
  --name my-muwanx-app \
  --resource-group my-resource-group \
  --location eastus2 \
  --app-location "dist"
```

### GitHub Actions

Azure automatically creates a workflow when you connect your repository.

## Custom Domain

### Netlify

1. Go to Domain settings in Netlify
2. Add custom domain
3. Configure DNS:
   - Add CNAME record pointing to `your-site.netlify.app`

### GitHub Pages

1. Add `CNAME` file to docs folder:

```
yourdomain.com
```

2. Configure DNS:
   - Add CNAME record pointing to `username.github.io`

### Vercel

1. Go to Domains in Vercel dashboard
2. Add domain
3. Follow DNS configuration instructions

## Performance Optimization

### Compression

Enable gzip/brotli compression on your server.

**Netlify**: Automatic

**GitHub Pages**: Automatic

**S3**: Configure manually:

```bash
aws s3 sync dist/ s3://bucket/ \
  --content-encoding gzip \
  --exclude "*" \
  --include "*.js" \
  --include "*.css"
```

### Caching

Set appropriate cache headers.

**Netlify** - `_headers` file:

```
/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
```

**Vercel** - `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### CDN

Use a CDN for global distribution:

- **Netlify**: Built-in CDN
- **Vercel**: Built-in edge network
- **CloudFront**: AWS CDN
- **Cloudflare**: Can proxy your site

## Security

### HTTPS

Always use HTTPS for production:

- **Netlify**: Automatic
- **Vercel**: Automatic
- **GitHub Pages**: Automatic
- **Custom domains**: Use Let's Encrypt or your provider's SSL

### Content Security Policy

Add CSP headers for security.

**Netlify** - `_headers`:

```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-eval'; worker-src 'self' blob:; style-src 'self' 'unsafe-inline'
```

### CORS

If loading external assets, configure CORS appropriately.

## Monitoring

### Netlify Analytics

Enable in Netlify dashboard for visitor insights.

### Google Analytics

Add to your deployment:

```python
# Inject Google Analytics (if customizing HTML)
analytics_code = """
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
"""
```

## Deployment Checklist

Before deploying to production:

- [ ] Test build locally
- [ ] Verify all assets load correctly
- [ ] Test on multiple browsers
- [ ] Test on mobile devices
- [ ] Check performance (load time)
- [ ] Verify policies work correctly
- [ ] Test VR functionality (if used)
- [ ] Configure custom domain
- [ ] Enable HTTPS
- [ ] Set up analytics
- [ ] Test from different geographic locations
- [ ] Configure caching headers
- [ ] Enable compression

## Continuous Deployment

### Build Script

Create a reusable `build.py`:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
import muwanx as mwx
import mujoco

def build(output_dir="./dist"):
    """Build the Muwanx application."""
    builder = mwx.Builder(base_path="/")

    # Add your projects here
    project = builder.add_project(name="Demo")
    # ... add scenes ...

    # Build
    app = builder.build(output_dir=output_dir)
    print(f"✓ Build complete: {output_dir}")
    return app

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "./dist"
    build(output)
```

### Pre-deployment Tests

```python
def test_build():
    """Test that build produces expected files."""
    app = build(output_dir="./test_dist")

    # Check files exist
    from pathlib import Path
    dist = Path("test_dist")

    assert (dist / "index.html").exists()
    assert (dist / "config.json").exists()
    assert (dist / "assets").exists()

    print("✓ Build tests passed")

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        test_build()
    else:
        build()
```

## Troubleshooting

### Assets Not Loading

Check `base_path` matches deployment location:

```python
# Wrong
builder = mwx.Builder(base_path="/")  # But deployed to /myapp/

# Correct
builder = mwx.Builder(base_path="/myapp/")
```

### 404 Errors

Configure server to serve `index.html` for all routes.

### CORS Issues

Ensure ONNX and model files have correct CORS headers.

### Slow Loading

- Optimize mesh file sizes
- Reduce ONNX model size
- Enable compression
- Use CDN

## See Also

- [Building Projects](../user-guide/building-projects.md) - Build configuration
- [VR Support](vr-support.md) - Enable VR features
- [Getting Started](../getting-started.md) - Installation and quick start
