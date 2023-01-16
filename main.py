import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
from pathlib import Path


def get_coordinates(catalog_dir: Path): 
    """
    This function returns a list of boundaries for every image as [[lon, lat], [lon, lat], [lon, lat], etc.] in the catalog. 
    """
    #catalog_list=os.listdir(catalog_dir)
    all_coordinates=[]
    catalogs = catalog_dir.glob('*.json')
    for catalog in catalogs:
        with open(catalog) as f:
            catalog_json=json.load(f)
        coordinates_list=catalog_json['geometry']['coordinates'][0]
        lon=[coordinates[0] for coordinates in coordinates_list]
        all_coordinates.append(lon)
        lat=[coordinates[1] for coordinates in coordinates_list]
        all_coordinates.append(lat)
                    # parse out coordinates
            
    return all_coordinates


def plot_coordinates(coords:list):
    # create figure
    plt.figure(figsize=(15, 10))

    # create a Basemap
    m=Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180)

    # display blue marble image
    m.bluemarble(scale=0.2) # 0.2 downsamples to 1350x675 image
    m.drawcoastlines(color='white', linewidth=0.2) # add coastlines
    m.drawparallels(range(-90, 90, 10), labels=[0, 1, 0, 0], color='white', textcolor='black')
    m.drawmeridians(range(-180, 180, 10), labels=[0, 0, 0, 1], color='white', textcolor='black', rotation=90)

    # flatten lat and lon coordinate lists
    image_lon=[coords[x] for x in range(len(coords)) if x%2==0]
    image_lon=np.concatenate(image_lon).ravel()
    image_lat=[coords[x] for x in range(len(coords)) if x%2==1]
    image_lat=np.concatenate(image_lat).ravel()

    # convert lon/lat to x/y map projection coordinates
    x, y=m(image_lon, image_lat)
    plt.scatter(x, y, s=10, marker='o', color='Red') 

    plt.title('Data Distribution')
    plt.show()
    print("P")




def main(PROJECT_DIRECTORY: Path):
    image_catalog_dir=Path(PROJECT_DIRECTORY / 'catalog')
    image_dir=Path(PROJECT_DIRECTORY /  'images')

    coords = get_coordinates(image_catalog_dir)
    plot_coordinates(coords)
    

    


if __name__ == '__main__':
    PROJECT_DATA_DIR = Path('C:/vscode_projects/nvidia/flood_data')
    main(PROJECT_DATA_DIR)