function bits= expGolombSigned(N)
%Exp Golomb code for non-negative numbers

if N>0
    bits = expGolombUnsigned(2*N-1);
else
    bits = expGolombUnsigned(-2*N);
end
