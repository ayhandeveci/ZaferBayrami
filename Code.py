import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import requests
from io import BytesIO
import time

# GeoJSON dosyasının GitHub URL'si
github_geojson_url = "https://raw.githubusercontent.com/ayhandeveci/ZaferBayrami/main/turkey-admin-level-4.geojson"

# GeoJSON verisini çekme
response = requests.get(github_geojson_url)
geojson_data = response.json()

# GeoDataFrame oluşturma
city_gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

# İlgili şehirleri belirle
target_cities = [
    'Afyonkarahisar', 'Kütahya', 'Eskişehir', 'Uşak', 'Balıkesir',
    'Bursa', 'Bilecik', 'Sakarya', 'Düzce', 'Bolu', 'İzmir'
]

# Renkler için sözlük oluşturma
city_colors = {city: 'red' for city in city_gdf['name']}  # Tüm şehirleri başlangıçta kırmızı yap

# Hedef şehirleri sarı yap
for city in target_cities:
    city_colors[city] = 'yellow'

# Haritayı çizdirmek için fonksiyon
def draw_map():
    ax.clear()
    city_gdf.plot(ax=ax, color='red', edgecolor='white')
    for city in city_gdf['name']:
        city_color = city_colors[city]
        city_gdf[city_gdf['name'] == city].plot(ax=ax, color=city_color, edgecolor='white')
    ax.set_title('Türkiye Haritası - İl Sınırları')
    ax.set_axis_off()
    plt.draw()

# Buton fonksiyonu güncellemesi
animation_speed = 0.1  # Saniye cinsinden bekleme süresi

def animate_colors(event):
    global city_colors
    toggle_button.set_active(False)  # Animasyon sırasında buton etkin değil
    for i in range(len(target_cities)):
        city = target_cities[i]
        city_colors[city] = 'red'  # Şehirleri sırayla kırmızı yap
        print(f"Renk değiştirilen şehir: {city}")  # Şehir ismini print et
        draw_map()
        plt.pause(animation_speed)
        toggle_button.label.set_text(city)  # Buton üzerinde şehir adını güncelle
        toggle_button.ax.figure.canvas.draw()  # Buton görüntüsünü güncelle
        time.sleep(animation_speed)  # Bekleme süresi ekle
    toggle_button.set_active(True)  # Animasyon bittiğinde buton tekrar etkin

# Haritayı çizdir
fig, ax = plt.subplots(figsize=(12, 8))
draw_map()  # İlk haritayı çizdir


button_ax = plt.axes([0.45, 0.05, 0.1, 0.15], frameon=False)

response = requests.get("https://raw.githubusercontent.com/ayhandeveci/ZaferBayrami/main/button.png")
button_image = Image.open(BytesIO(response.content))
button_image = button_image.resize((button_image.width // 2, button_image.height // 2))

button_imagebox = OffsetImage(button_image, zoom=0.15)
button_annotation = AnnotationBbox(button_imagebox, (0.5, 0.5), frameon=False, boxcoords="axes fraction")
button_ax.add_artist(button_annotation)

# Butonun boyutunu değiştirerek tıklama efekti ver
def on_button_click(event):
    animate_colors(None)  # Butona tıklandığında işlemi başlat

toggle_button = Button(button_ax, '', hovercolor='none')  # Hover efektini kaldır
toggle_button.label.set_fontsize(0)
toggle_button.on_clicked(on_button_click)  # Butona tıklandığında bu fonksiyonu çağır

plt.show()
