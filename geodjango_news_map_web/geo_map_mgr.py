import folium
import geopandas as gp
import numpy as np
import pandas as pd
import pycountry
import os

from logging import Logger
from datetime import datetime
from geodjango_news_map.settings import STATIC_ROOT, BASE_DIR

logger = Logger(__name__)

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(SETTINGS_DIR))
# CHORO_MAP_ROOT = os.path.join(PROJECT_ROOT, 'geodjango_news_map_web/media/')
CHORO_MAP_ROOT = os.path.join(BASE_DIR, 'geodjango_news_map_')

class GeoMapManager:

    @staticmethod
    def map_source(source_country):
        return (pycountry.countries.get(alpha_2=str(source_country).upper())).alpha_3 if source_country else None


    def build_choropleth(self, argument, focus, geo_data_mgr):
        world_df = gp.read_file(geo_data_mgr.filename)
        global_map = folium.Map(location=[0, 0], tiles='OpenStreetMap', zoom_start=3)
        articles_per_country = pd.Series(geo_data_mgr.result_dict)
        world_df['article_count'] = world_df['id'].map(articles_per_country)
        world_df.head()
        world_df.plot(column='article_count')

        threshold_scale = self.get_threshold(articles_per_country)

        folium.Choropleth(geo_data=geo_data_mgr.json_data,
                          name='choropleth',
                          data=world_df,
                          columns=['id', 'article_count'],
                          key_on='feature.id',
                          fill_color='PuBuGn',
                          bins=[float(x) for x in threshold_scale],  # https://github.com/python-visualization/folium/issues/1130
                          fill_opacity=0.7,
                          line_opacity=0.2).add_to(global_map)
                            # YlGrBu - RdYlGn - YlOrBr - RdYlBu - PuBuGn - YlOrRd
                            # Oranges - Greens -Purples - Reds - Greys - Blues
                            # Pastel1 - Pastel2 - Spectral - Set1 - Set2 - Set3 - Dark2

        folium.TileLayer("stamenwatercolor", attr='attr').add_to(global_map)
        folium.TileLayer("stamenterrain", attr='attr').add_to(global_map)
        folium.TileLayer("cartodbpositron", attr='attr').add_to(global_map)
        folium.TileLayer("OpenStreetMap", attr='attr').add_to(global_map)
        folium.LayerControl().add_to(global_map)

        filename = f"{datetime.ctime(datetime.now()).replace(' ', '_').replace(':', '-')}_{focus}_query_{argument}_choropleth_map.html"
        global_map.save(CHORO_MAP_ROOT + filename)
        # global_map.save(f'templates/maps/{filename[0:-5]}.html')
        choro_html = global_map.get_root().render()

        # return global_map, choro_html, filename if self.choro_to_file(choro_html, filename) else None
        return global_map._repr_html_(), filename, global_map if global_map and filename else None


    @staticmethod
    def get_threshold(articles_per_country):

        if articles_per_country.values.max() <= 16:
            threshold_scale = np.linspace(
                articles_per_country.values.min(), articles_per_country.values.max(), 6, dtype=int).tolist()

        elif 160 >= articles_per_country.values.max() > 16:
            threshold_scale = [0, 1,
                               articles_per_country.values.max() // 8,
                               articles_per_country.values.max() // 4,
                               articles_per_country.values.max() // 2,
                               articles_per_country.values.max()]

        elif articles_per_country.values.max > 160:
            threshold_scale = [0, 1, 2, 5, 10, articles_per_country.values.max()]

        else:
            logger.error('threshold-scale not being set in choropleth by articles_per_country.max')
            threshold_scale = [0, 1, 2, 3, 4, 5]

        return threshold_scale



    @staticmethod
    def choro_to_file(choro_html, filename):
        try:
            with open(CHORO_MAP_ROOT+filename, "w") as file:
                file.write(choro_html)
                return True
        except FileNotFoundError as e:
            logger.exception(f'{e} while writing map to file')
            return False
