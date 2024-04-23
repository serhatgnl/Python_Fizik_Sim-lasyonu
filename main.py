import pygame
from random import randrange
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False

COZ = GENISLIK, YUKSEKLIK = 1600, 900
FPS = 60

pygame.init()

yuzey = pygame.display.set_mode(COZ)
clock = pygame.time.Clock()
cizim_secenk = pymunk.pygame_util.DrawOptions(yuzey)


alan = pymunk.Space()
alan.gravity = 0, 4000
top_kutle, top_yaricap = 500, 50
segment_kalinlik = 8

a, b, c, d, e, f = 50, 50, 300, 40, 80, 50
x1, x2, x3, x4, x5, x6 = a, GENISLIK // 2 - c, GENISLIK // 2 - e, GENISLIK // 2 + e, GENISLIK // 2 + c, GENISLIK - a
y1, y2, y3, y4, y5, y6, y7 = b, YUKSEKLIK // 6 - d, YUKSEKLIK // 6, YUKSEKLIK // 4 - f, YUKSEKLIK // 4, YUKSEKLIK // 2 - 2 * b, YUKSEKLIK - 2 * b
M1, M2, M3, M4, M5, M6 = (x1, -60), (x1, y1), (x2, y2), (x2, y3), (x3, y4), (x3, y5)
N1, N2, N3, N4, N5, N6 = (x6, -100), (x6, y1), (x5, y2), (x5, y3), (x4, y4), (x4, y5)
S1, S2 = (0, YUKSEKLIK), (GENISLIK, YUKSEKLIK)


def top_olustur(alan, pos):
    top_moment = pymunk.moment_for_circle(top_kutle, 0, top_yaricap)
    top_govde = pymunk.Body(top_kutle, top_moment)
    top_govde.position = pos   
    top_nesne = pymunk.Circle(top_govde, top_yaricap)
    top_nesne.color = pygame.color.THECOLORS['red']
    top_nesne.elasticity = 0.6
    top_nesne.friction = 0.4
    alan.add(top_govde, top_nesne)

def segment_olustur(from_, to_, kalinlik, alan, renk):
    segment_nesne = pymunk.Segment(alan.static_body, from_, to_, kalinlik)
    segment_nesne.color = pygame.color.THECOLORS[renk]
    segment_nesne.elasticity = 0.6
    segment_nesne.friction = 0.4
    alan.add(segment_nesne)


kutu_kutle, kutu_boyut = 20, (100, 80)
for x in range(140, GENISLIK - 60, kutu_boyut[0]):
    for y in range(YUKSEKLIK - 150, YUKSEKLIK - 20, kutu_boyut[1]):
        kutu_moment = pymunk.moment_for_box(kutu_kutle, kutu_boyut)
        kutu_govde = pymunk.Body(kutu_kutle, kutu_moment)
        kutu_govde.position = x, YUKSEKLIK - 100 
        kutu_nesne = pymunk.Poly.create_box(kutu_govde, kutu_boyut)
        kutu_nesne.elasticity = 0.6
        kutu_nesne.friction = 0.4
        kutu_nesne.color = [randrange(256) for i in range(4)]
        alan.add(kutu_govde, kutu_nesne)

SEGMENTS = (M1, M2), (M2, M3), (M3, M4), (M4, M5), (M5, M6), (N1, N2), (N2, N3), (N3, N4), (N4, N5), (N5, N6)
for segment in SEGMENTS:
    segment_olustur(*segment, segment_kalinlik, alan, 'darkorange')
segment_olustur(S1, S2, 20, alan, 'darkorange')
segment_olustur((0, YUKSEKLIK), (GENISLIK, YUKSEKLIK), 50, alan, 'darkorange')



while True:
    yuzey.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                top_olustur(alan, event.pos)
                

    alan.step(1/FPS)
    alan.debug_draw(cizim_secenk)


    
    pygame.display.flip()
    clock.tick(FPS)
