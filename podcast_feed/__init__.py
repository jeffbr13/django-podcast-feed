from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

VERSION = '0.0.2'
NAME = 'django-podcast-feed'
DESCRIPTION = 'Generate Apple Podcasts-compatible syndication feeds.'


class ItunesPodcastRssFeed(Rss201rev2Feed):
    def __init__(self, title, link, description, language=None, author_email=None,
                 author_name=None, author_link=None, subtitle=None, categories=None,
                 feed_url=None, feed_copyright=None, feed_guid=None, ttl=None,
                 artwork_link=None, category=None, explicit=None, owner_name=None, owner_email=None,
                 **kwargs):
        super().__init__(title, link, description, language, author_email,
                         author_name, author_link, subtitle, categories,
                         feed_url, feed_copyright, feed_guid, ttl, **kwargs)
        self.feed['artwork_link'] = artwork_link
        self.feed['itunes_category'] = category
        self.feed['explicit'] = explicit
        self.feed['owner_name'] = owner_name
        self.feed['owner_email'] = owner_email

    def root_attributes(self):
        attrs = super().root_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        return attrs

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.addQuickElement('itunes:image', attrs={'href': self.feed.get('artwork_link', '')})
        handler.addQuickElement('itunes:subtitle', self.feed.get('subtitle', ''))
        handler.addQuickElement('itunes:summary', self.feed.get('description', ''))
        handler.addQuickElement('itunes:category', attrs={'text': self.feed.get('itunes_category', '')})
        handler.addQuickElement('itunes:keywords', ', '.join(self.feed.get('categories', [])))
        handler.addQuickElement('itunes:explicit', 'yes' if self.feed.get('explicit') else 'clean')
        handler.addQuickElement('itunes:author', self.feed.get('author_name'))

        handler.startElement('itunes:owner', {})
        handler.addQuickElement('itunes:name', self.feed.get('owner_name'))
        handler.addQuickElement('itunes:email', self.feed.get('owner_email'))
        handler.endElement('itunes:owner')

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        if item.get('description'):
            handler.addQuickElement('itunes:summary', item.get('description'))
        if item.get('author_name'):
            handler.addQuickElement('itunes:author', item.get('author_name'))
        if item.get('duration'):
            handler.addQuickElement('itunes:duration', item.get('duration'))


class PodcastFeed(Feed):
    """Custom Feed subclass for Apple Podcasts format.

    Set the following attributes on your subclass:

    - artwork_link
    - itunes_category
    - explicit
    - owner_name
    - owner_email
    """
    feed_type = ItunesPodcastRssFeed

    def get_feed(self, obj, request):
        feed = super().get_feed(obj, request)
        feed.feed['artwork_link'] = self._get_dynamic_attr('artwork_link', obj)
        feed.feed['itunes_category'] = self._get_dynamic_attr('itunes_category', obj)
        feed.feed['explicit'] = self._get_dynamic_attr('explicit', obj)
        feed.feed['owner_name'] = self._get_dynamic_attr('owner_name', obj)
        feed.feed['owner_email'] = self._get_dynamic_attr('owner_email', obj)
        return feed

    def item_extra_kwargs(self, item):
        extra_kwargs = super().item_extra_kwargs(item)
        extra_kwargs['duration'] = str(self._get_dynamic_attr('item_duration', item))
        return extra_kwargs
