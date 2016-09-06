"""
I wanted to import a couple of things by default
for ease of use.

Instead of doing:
    from webbridge.bridge import Bridge, blow
Importing them here allows you to:
    from webbridge import Bridge, blow
    
If there's a simpler, more Pythonic way, let your pal know.
"""
from bridge import Bridge, blow
