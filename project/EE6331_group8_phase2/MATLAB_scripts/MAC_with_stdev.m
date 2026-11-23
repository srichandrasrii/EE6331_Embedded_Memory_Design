load( 'weightsAndBiases.mat', 'W1', 'b1', 'W2', 'b2' ) ;
%% load test set images and labels
images = loadMNISTImages( 't10k-images' ) ;
labels = loadMNISTLabels( 't10k-labels' )' ;
load("stdev_of_MACs.mat");
images=fi(images,1,4,3);
images=double(images);
W1=fi(W1,1,7,4);
%%images>>>1 column = 1 input
%%weights>>>1 row = 1 vector
%% Layer 1
W1_bitwise=zeros(100,784,7);
for k=1:7
    t1=bitget(W1,k);
    for j=1:size(W1,2)
        for i=1:size(W1,1)
            W1_bitwise(i,j,k)=t1(i,j);  
        end
    end
end
t2=zeros(1,784);

MACS=zeros(100,10000,7);
for i=1:100
    for j=1:10000
        for k=1:7
            MACS(i,j,k)=W1_bitwise(i,:,k)*images(:,j);
        end
    end
end
%maximum MAC is 143.6250
%MAC passed through ADC
i=121;
clip=0:1:max(MACS,[],'all');
MACSclipped=MACS;
MACSclipped(MACSclipped>clip(i))=clip(i);
MACSclipped=MACSclipped/clip(i);
MACSq=fi(MACSclipped,1,8,7);
MACSq=double(MACSq);
MACSq=MACSq*clip(i);
for k=1:121
    MACSq(MACSq<(k)&MACSq>=(k-1))=MACSq(MACSq<(k)&MACSq>=(k-1))+517.417*normrnd(0,unnamed2(i));
end
%summation of MACS
MACS_summed=-MACSq(:,:,7)*(2^(6));
for i=1:6
    MACS_summed=MACS_summed+(MACSq(:,:,i)*(2^(i-1)));
end
%z1 = W1 * images + b1 ;
z1 = MACS_summed*(2^(-4)) + b1 ;
a1 = max( 0, z1 ) ;
%% Layer 2
z2 = W2 * a1 + b2 ;
[ ~, guesses ] = max( z2, [], 1 ) ; guesses = guesses - 1 ;
%% Get accuracy
NumMatches = sum( labels == guesses ) ;
Acc = NumMatches / numel( labels ) * 100 ;
%% Display Accuracy
display( Acc ) ;