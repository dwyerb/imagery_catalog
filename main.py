import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
from pathlib import Path


def get_extent(file_path: Path):
    """
    This function returns the extent as [left, right, bottom, top] for a given image. 
    """
    # read catalog for image
    #with open(file_path) as f:
    with file_path.open() as f:
        catalog_json=json.load(f)
    coordinates=catalog_json['geometry']['coordinates'][0]
    coordinates=np.array(coordinates)
    # get boundaries
    left=np.min(coordinates[:, 0])
    right=np.max(coordinates[:, 0])
    bottom=np.min(coordinates[:, 1])
    top=np.max(coordinates[:, 1])
    return left, right, bottom, top

def tiles_by_region(region_name: str, project_path:Path, plot_type='images'): 
    """# set catalog and images/masks path
    catalog_dir=os.path.join(os.getenv('LOCAL_DATA_DIR'), 'catalog', 'sen1floods11_hand_labeled_source')
    if plot_type=='images': 
        dir=os.path.join(image_dir, 'all_images')
        cmap='viridis'
    elif plot_type=='masks': 
        dir=os.path.join(mask_dir, 'all_masks')
        cmap='gray'
    else: 
        raise Exception('Bad Plot Type')"""

    cmap='viridis'

    image_path = Path(project_path / "images")
    json_dir = Path(project_path / "catalog")

    # initiate figure boundaries, which will be modified based on the extent of the tiles
    x_min, x_max, y_min, y_max=181, -181, 91, -91
    fig=plt.figure(figsize=(15, 15))
    ax=plt.subplot(111)
    
    # iterate through each image/mask and plot
    file_list=os.listdir(image_path)
    for each_file in file_list:
        # check if image/mask is related to region and a .png file
        print(each_file.split('.')[-1])
        print(each_file.split('_')[0])
        if (each_file.split('.')[-1]=='png') & (each_file.split('_')[0]==region_name): 
            # get boundaries of the image
            #extent=get_extent(f"{image_path}/{each_file.split('.')[0]}/{each_file.split('.')[0]}.json")
            json_path = Path(json_dir / f"{each_file.split('.')[0]}_label.json")
            #extent=get_extent(f"{image_path}/{each_file.split('.')[0]}/{each_file.split('.')[0]}.json")
            extent=get_extent(json_path)
            x_min, x_max=min(extent[0], x_min), max(extent[1], x_max)
            y_min, y_max=min(extent[2], y_min), max(extent[3], y_max)
            image=mpimg.imread(f'{image_path}/{each_file}')
            plt.imshow(image, extent=extent, cmap=cmap)

    # set boundaries of the axis
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    plt.show()
    print("P")



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

    #coords = get_coordinates(image_catalog_dir)
    #plot_coordinates(coords)

    tiles_by_region("Spain", PROJECT_DIRECTORY, "meh")


    print("")
       


if __name__ == '__main__':
    PROJECT_DATA_DIR = Path('C:/vscode_projects/nvidia/flood_data')
    main(PROJECT_DATA_DIR)