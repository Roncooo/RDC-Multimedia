function [ampSpectrum, freq] = CTFT_real(x,Fc, N, xaxis)
%CTFT_real calcola i campioni della Continuos Time Fourier transform del
%segnale reale x a partire dai suoi campioni presi con frequenza Fc
%
%[ampSpectrum, freq] = CTFT_real(x,Fc)
%     x - contiene i campioni del segnale da analizzare
%    Fc - è la frequenza di campionamento in Hz con cui sono stati prodotti
%    i valori di x
%
%    ampSpectrum - campioni dello spettro di ampiezza tra 0 e Fc/2.
%    freq - i valori di frequenza corrispondenti
%
%Parametri opzionali
%[ampSpectrum, freq] = CTFT_real(x,Fc, N)
%  N permette di ottenere un numero di campioni dello spettro diverso dal
%  default. Per default, il numero di campioni è uno più la più
%  piccola potenza di due  non inferiore al numero di campioni di x.
%  Se si specifica un valore di N intero positivo, il numero di campioni
%  sarà 1+2^(N+M), dove 2^M è la più piccola potenza di 2 non inferiore al
%  numero di campioni di x
%
%[ampSpectrum, freq] = CTFT_real(x,Fc, N, xaxis)
%  se xaxis = 'puls' oppure xaxis = 'omega', la variabile di uscita freq
%  esprime i valori di pulsazione corrispondenti allo spettro di ampiezza
%
% Esempio
% %% Creazione di un segnale con FC = 1kHz. Sinusoide a 5Hz, troncata.
% TC = 1e-3;
% t=0:TC:10;
% f0 = 5;
% x = (abs(t-2)<1/2).*cos(f0*2*pi*t);
% %% Calcolo della TF
% [X,F]=CTFT_real(x,1/TC);
% %% Grafico della TF
% plot(F,X);
% axis([0 100 0 1/2]) % Questo comando fa uno zoom sulle freq da 0 a 100Hz
%
%
% (C) 2024 M. Cagnazzo
%

% Controllo parametri d'ingresso
if nargin <4, xaxis = 'freq'; end
if nargin <3, M = 2^nextpow2(numel(x)+1); else M=2^nextpow2(numel(x)+1+N ); end
if nargin <2, error('Fornire due parametri d''ingresso'); end

fStep = Fc/M;
freq = 0:fStep:(Fc/2);

X = abs(fft(x,M))/Fc;
ampSpectrum =  abs(X(1:M/2+1));

switch xaxis
    case {'puls', 'omega'}
        freq = freq*2*pi;
end
end