import sys; from PIL import Image
fs=sys.argv[2:]; out=sys.argv[1]; cols=3; w=640
ims=[Image.open(f).convert('RGB') for f in fs]; ims=[i.resize((w,int(i.height*w/i.width))) for i in ims]
h=max(i.height for i in ims); rows=(len(ims)+cols-1)//cols
G=Image.new('RGB',(cols*w,rows*h),'white')
for k,i in enumerate(ims): G.paste(i,((k%cols)*w,(k//cols)*h))
G.save(out)
