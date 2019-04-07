from PIL import Image, ImageEnhance
from resizeimage import resizeimage
import numpy

#PARAMETRI:
vSlike=0.13 #velikost slike v metrih
vKonice=0.001 #velikost konice v metrih

#koordinate zgornje desne točke:
k=[0.0658,-0.4489,0.1380]#BASE!
#višina ko ne gravira:
vis=0.15
#pospešek
a=1.3
#rotacija orodja
r=[2.206,-2.364,2.455]

#hitrosti:
hc=0.004 #črna
hs=0.010 #siva
hss=0.020 #svetlo siva
hp=0.3 #hitrost vmesnega premikanja

#čakanje za črno piko:
cp=0.4
#čakanje za sivo piko:
sp=0.2
#čakanje za svetlo sivo piko:
ssp=0.1

#kontrast slike
kontrast=1.5
#svetlost slike
svetlost=1.4
#ostrost slike
ostrost=4

vImg=int(vSlike/vKonice)
img = Image.open('photo.jpg')

img=img.transpose(Image.FLIP_LEFT_RIGHT)

contrast = ImageEnhance.Contrast(img)
img=contrast.enhance(kontrast)
brightness=ImageEnhance.Brightness(img)
img=brightness.enhance(svetlost)

img=resizeimage.resize_contain(img, [vImg, vImg])
sharpness=ImageEnhance.Sharpness(img)
img=sharpness.enhance(ostrost)

img=img.convert('L')
#img.show()

data=numpy.asarray(img)
data.setflags(write=1)

#doloci da so 4 bavre
for i in range(0,vImg):
	for j in range(0,vImg):
		if data[i,j]<42:
			data[i,j]=0 #crna
		elif data[i,j]>=42 and data[i,j]<127:
			data[i,j]=85 #siva
		elif data[i,j]>=127 and data[i,j]<212:
			data[i,j]=170 #ssiva
		else:
			data[i,j]=255 #bela

img = Image.fromarray(data, 'L')
img.show()

#rabimo 6 datotek, drugace robot zasteka
dat1=""
dat2=""
dat3=""
dat4=""
dat5=""
dat6=""

stevec=0 #steje vrstice
preklopiPrej=100 #koliko vrstic prej preklopi
datNum=1


def shraniTekst(tekst):
	global dat1, dat2, dat3, dat4, dat5, dat6, datNum
	if datNum==1: dat1=dat1+tekst
	elif datNum==2: dat2=dat2+tekst
	elif datNum==3: dat3=dat3+tekst
	elif datNum==4: dat4=dat4+tekst
	elif datNum==5: dat5=dat5+tekst
	else: dat6=dat6+tekst


def pika(i,j,spanje):
	global stevec, datNum

	x=k[0]+vKonice/2+vKonice*i
	y=k[1]-vKonice/2-vKonice*j
	x=round(x,4)
	y=round(y,4)
	tekst=f'movel(p[{x},{y},{vis},{r[0]},{r[1]},{r[2]}], a={a}, v={hp})\nmovel(p[{x},{y},{k[2]},{r[0]},{r[1]},{r[2]}], a={a}, v={hp})\nsleep({spanje})\nmovel(p[{x},{y},{vis},{r[0]},{r[1]},{r[2]}], a={a}, v={hp})\n'
	
	if stevec>=(1000-preklopiPrej): 
		datNum=datNum+1
		stevec=0

	shraniTekst(tekst)

	stevec=stevec+4

	if stevec>=(1000-preklopiPrej): 
		datNum=datNum+1
		stevec=0

	

def zacetek(i,j):
	global stevec, datNum

	x=k[0]+vKonice/2+vKonice*i
	y=k[1]-vKonice/2-vKonice*j
	x=round(x,4)
	y=round(y,4)
	tekst=f"movel(p[{x},{y},{vis},{r[0]},{r[1]},{r[2]}], a={a}, v={hp})\nmovel(p[{x},{y},{k[2]},{r[0]},{r[1]},{r[2]}], a={a}, v={hp})\n"

	stevec=stevec+2

	if stevec>=(1000-preklopiPrej): 
		datNum=datNum+1
		stevec=0

	shraniTekst(tekst)


def konec(i,j,hitrost):
	global stevec, datNum

	x=k[0]+vKonice/2+vKonice*i
	y=k[1]-vKonice/2-vKonice*j
	x=round(x,4)
	y=round(y,4)
	tekst=f"movel(p[{x},{y},{k[2]},{r[0]},{r[1]},{r[2]}], a={a}, v={hitrost})\nmovel(p[{x},{y},{vis},{r[0]},{r[1]},{r[2]}], a={a}, v={hp})\n"

	shraniTekst(tekst)

	stevec=stevec+2

	if stevec>=(1000-preklopiPrej): 
		datNum=datNum+1
		stevec=0


def prehod(i,j,hitrost):
	global stevec, datNum

	x=k[0]+vKonice/2+vKonice*i
	y=k[1]-vKonice/2-vKonice*j
	x=round(x,4)
	y=round(y,4)
	tekst=f"movel(p[{x},{y},{k[2]},{r[0]},{r[1]},{r[2]}], a={a}, v={hitrost})\n"
	
	shraniTekst(tekst)

	stevec=stevec+1


for i in range(0,vImg):

	for j in range(0,vImg):

		if data[i,j]!=255:

			if j==0: #na prvem robu

				if data[i,j+1]==255: #pika

					if data[i,j]==0: pika(i,j,cp)#crna
					if data[i,j]==85: pika(i,j,sp)#siva
					if data[i,j]==170: pika(i,j,ssp)#svetlo siva
			
				else: #začetek

					zacetek(i,j)

			elif j==int((vImg-1)): #na zadnjem robu

				if data[i,j-1]==255: #pika

					if data[i,j]==0: pika(i,j,cp)#crna
					if data[i,j]==85: pika(i,j,sp)#siva
					if data[i,j]==170: pika(i,j,ssp)#svetlo siva

				else: #konec

					if data[i,j]==0: konec(i,j,hc)#crna
					if data[i,j]==85: konec(i,j,hs)#siva
					if data[i,j]==170: konec(i,j,hss)#svetlo siva

			elif data[i,j-1]==255 and data[i,j+1]==255: #pika
				
				if data[i,j]==0: pika(i,j,cp)#crna
				if data[i,j]==85: pika(i,j,sp)#siva
				if data[i,j]==170: pika(i,j,ssp)#svetlo siva
			
			elif data[i,j-1]==255: #začetek
				zacetek(i,j)

			elif data[i,j+1]==255: #konec

				if data[i,j]==0: konec(i,j,hc)#crna
				if data[i,j]==85: konec(i,j,hs)#siva
				if data[i,j]==170: konec(i,j,hss)#svetlo siva

			elif data[i,j+1]!=data[i,j]: #prehod

				if data[i,j]==0: prehod(i,j,hc)#crna
				if data[i,j]==85: prehod(i,j,hs)#siva
				if data[i,j]==170: prehod(i,j,hss)#svetlo siva



file = open('koda1.script','w')
file.write(dat1)
file.close()

file = open('koda2.script','w')
file.write(dat2)
file.close()

file = open('koda3.script','w')
file.write(dat3)
file.close()

file = open('koda4.script','w')
file.write(dat4)
file.close()

file = open('koda5.script','w')
file.write(dat5)
file.close()

file = open('koda6.script','w')
file.write(dat6)
file.close()

print("Koncano")
#ce ne bo ok daj smer skos na 1