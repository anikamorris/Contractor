  
from unittest import TestCase, main, mock
from bson.objectid import ObjectId
from app import app

sample_product_id = ObjectId('5d9fb2bf5611971e503ac064')
sample_product = {
    "id":740,
    "brand":"dior",
    "name":"\n                            Junon\n                            ",
    "price":"20.0",
    "price_sign":"£",
    "currency":"GBP",
    "image_link":"https://www.dior.com/beauty/version-5.1432748111912/resize-image/ep/0/214/90/0/v6_packshots_sku_pdg%252FPDG_Y0002959-F000355494.jpg",
    "product_link":"https://www.dior.com/beauty/en_gb/fragrance-beauty/makeup/nails/nail-lacquers/pr-naillacquers-y0002959_f000355494-couture-colour-gel-shine-long-wear.html",
    "website_link":"https://www.dior.com",
    "description":"Discover the new-generation Dior Vernis and its ingenious formula that plays up the gel effect.",
    "product_type":"nail_polish",
    "created_at":"2017-12-03T23:24:03.403Z",
    "updated_at":"2017-12-23T20:59:02.537Z",
    "product_api_url":"http://makeup-api.herokuapp.com/api/v1/products/740.json",
    "api_featured_image":"//s3.amazonaws.com/donovanbailey/products/api_featured_images/000/000/740/original/data?1514062742",
    "product_colors":[{"hex_value":"#A10705","colour_name":"999 Rouge 999"},
                    {"hex_value":"#340000","colour_name":"970 Nuit 1947"},
                    {"hex_value":"#780C18","colour_name":"853 Massaï"},
                    {"hex_value":"#C60F54","colour_name":"769 Front Row"},
                    {"hex_value":"#C90206","colour_name":"754 Pandore"},
                    {"hex_value":"#DB1057","colour_name":"669 Fizz Pink"},
                    {"hex_value":"#E40B6E","colour_name":"661 Bonheur"},
                    {"hex_value":"#E40040","colour_name":"659 Lucky"},
                    {"hex_value":"#E83B53","colour_name":"575 Wonderland"},
                    {"hex_value":"#E61E32","colour_name":"551 Aventure"},
                    {"hex_value":"#E73326","colour_name":"537 Riviera"},
                    {"hex_value":"#617686","colour_name":"494 Junon"},
                    {"hex_value":"#D2A896","colour_name":"413 Grège"},
                    {"hex_value":"#977D7B","colour_name":"403 Palais Royal"},
                    {"hex_value":"#A3948B","colour_name":"306 Trianon"},
                    {"hex_value":"#952D73","colour_name":"338 Mirage"},
                    {"hex_value":"#B63853","colour_name":"785 Cosmopolite"},
                    {"hex_value":"#F7B6B6","colour_name":"268 Ruban"},
                    {"hex_value":"#F9C8C8","colour_name":"155 Tra-la-la"},
                    {"hex_value":"#EA4D54","colour_name":"445 Coral Crush"},
                    {"hex_value":"#FCD9CB","colour_name":"108 Muguet"}]
    }

class ContractorTest(TestCase):
    def setUp(self):
        """Run before every test"""
        # Set up flask test client
        self.client = app.test_client()

        # Show flask errors that happen during tests
        app.config['TESTING'] = True

    def test_products_index(self):
        """Test the homepage of cosmetix"""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_products(self, mock_find):
        """Test showing a single product."""
        mock_find.return_value = sample_product

        result = self.client.get(f'/products/{sample_product_id}')
        self.assertEqual(result.status, '200 OK')

if __name__ == '__main__':
    main()