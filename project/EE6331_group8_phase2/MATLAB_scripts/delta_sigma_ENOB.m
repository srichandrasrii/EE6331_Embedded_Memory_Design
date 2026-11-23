MAC_ideal=linspace(0,120,121000);
Vout_range=linspace(0.79989626,0.5408729,121000);
load("Vout_values_real.mat");
MAC_values_meas=linspace(0,120,121);
Vout_interpolated=interp1(MAC_values_meas,Vout_data_real,MAC_ideal,"linear");
max_volt=max(Vout_data_real,[],"all");
Vout_interpolated=Vout_interpolated/max_volt;
Vout_quant=fi(Vout_interpolated,1,8,7);
Vout_quant=Vout_quant*max_volt;
Vout_interpolated=Vout_interpolated*max_volt;
Vout_quant=double(Vout_quant);
plot(MAC_ideal,Vout_range,'g');
hold on;
plot(MAC_ideal,Vout_quant,'r');
xlabel('MAC');
ylabel('voltage');
title("ideal voltage vs result");
error=Vout_range-Vout_quant;
LSB=(0.79989626-0.5408729)/(2^7);
std_byLSBpercent=(sqrt((error*error'/numel(Vout_quant))))/LSB;







