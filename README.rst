django-podcast-feed
===================

Extra attributes or methods to set on ``PodcastFeed``:

- ``subtitle``
- ``artwork_link``
- ``itunes_category``
- ``explicit``
- ``owner_name``
- ``owner_email``
- ``item_duration``

For example::

    MyPodcastFeed(podcast_feed.PodcastFeed):
        artwork_link = static('artwork.png')

        def get_items(self):
            Episode.objects.all()

        def item_duration(self, item):
            return item.duration_field

A more involved usage can be found in `jeffbr13/br-rss's views <https://github.com/jeffbr13/br-rss/blob/master/br_rss/boilerroomtv/views.py>`_.
