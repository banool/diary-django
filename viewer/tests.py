from django.test import TestCase  # noqa
from viewer.util import render_markdown

# These tests are all concerned with ensuring that the markdown is
# properly rendered into HTML.


class RenderTests(TestCase):
    ''' These test that the rendering works as expected. '''

    def test_secret(self):
        ''' Ensure that the <secret> tag works. '''
        secret_md = '''
hey pals!
<secret>
this is my big secret
</secret>
thanks for reading!
        '''
        rendered = render_markdown(secret_md)
        assert 'hey pals!' in rendered
        assert 'this is my big secret' not in rendered
        assert '<secret>' not in rendered
        assert '</secret>' not in rendered
        assert 'thanks for reading!' in rendered

    def test_secret_prepended_whitespace(self):
        ''' Ensure that the <secret> tag does NOT work if there are spaces
        before it. This is just the way it works, though perhaps it should
        work regardless of whitespace.
        '''
        secret_md = '''
        hey pals!
        <secret>
        this is my big secret
            </secret>
        thanks for reading!
        '''
        rendered = render_markdown(secret_md)
        assert 'hey pals!' in rendered
        assert 'this is my big secret' in rendered
        assert 'secret' in rendered
        assert '/secret' in rendered
        assert 'thanks for reading!' in rendered

    def test_link_conversion1(self):
        ''' Test that a Dropbox image link is properly converted into its
        dl.dropboxusercontent HTML tag counterpart. We don't expect this
        to work when the link isn't at the start of a line.
        '''
        link_md = '''
https://www.dropbox.com/s/v05retlqhjsauya/2016-11-25%2013.05.18.jpg?dl=0
        '''
        rendered = render_markdown(link_md)
        expected = (
            '<p><a href="https://www.dropbox.com/s/v05retlqhjsauya/2016-11-25%2013.05.18.jpg?dl=0">'
            '<img src="https://dl.dropboxusercontent.com/s/v05retlqhjsauya/2016-11-25%2013.05.18.jpg?dl=0" '
            'alt="" onload="this.width/=2;this.onload=null;"></a></p>'
        )
        assert rendered == expected

    def test_images_side_by_side(self):
        ''' When there are two dropbox image links on separate lines, we expect
        the output HTML to put them directly beside each other (no <p>).
        TODO What if the image links are multiple lines apart?
        '''
        pass


# These tests are for other Django'y things.
