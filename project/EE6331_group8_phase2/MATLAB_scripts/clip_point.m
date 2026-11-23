load("MACS.mat");
clip=0:1:max(MACS,[],'all');
MSE=zeros(1,144);
for i=1:144
    MACSclipped=MACS;
    MACSclipped(MACSclipped>clip(i))=clip(i);
    MACSclipped=MACSclipped/clip(i);
    MACSq=fi(MACSclipped,1,8,7);
    MACSq=double(MACSq);
    MACSq=MACSq*clip(i);
    error=MACS-MACSq;
    MSE(i)=mean(error.^2,'all');
end
plot(clip,MSE);
[M,I]=min(MSE);
display(I);