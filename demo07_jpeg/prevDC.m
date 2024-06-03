function previousBlockQuantizedDC = prevDC(quant_dct, rowPos,colPos); 
[R C] = size(quant_dct);
if colPos==1
    if rowPos==1,
        previousBlockQuantizedDC=0;
    else 
        previousBlockQuantizedDC = quant_dct(rowPos-8,C-7);
    end
else
    previousBlockQuantizedDC = quant_dct(rowPos,colPos-8);
end