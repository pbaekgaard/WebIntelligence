def findSitemaps(robotsTxtContent):

    sitemaps = []

    for line in robotsTxtContent.splitlines():
        line = line.strip()
        if line.lower().startswith("sitemap:"):
            sitemapUrl = line.split(":", 1)[1].strip() 
            sitemaps.append(sitemapUrl)
    
    return sitemaps