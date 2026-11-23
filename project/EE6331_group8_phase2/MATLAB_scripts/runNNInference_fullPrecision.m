load( 'weightsAndBiases.mat', 'W1', 'b1', 'W2', 'b2' ) ;
%% load test set images and labels
images = loadMNISTImages( 't10k-images' ) ;
labels = loadMNISTLabels( 't10k-labels' )' ;

%% Layer 1
z1 = W1 * images + b1 ;
a1 = max( 0, z1 ) ;
%% Layer 2
z2 = W2 * a1 + b2 ;
[ ~, guesses ] = max( z2, [], 1 ) ; guesses = guesses - 1 ;
%% Get accuracy
NumMatches = sum( labels == guesses ) ;

Acc = NumMatches / numel( labels ) * 100 ;

%% Display Accuracy
display( Acc ) ;