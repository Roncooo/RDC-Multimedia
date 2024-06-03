function bits = block_entropy_coding(blk,dc)
% Questa funzione effettua la codifica lossless di JPEG su un blocco 8x8
% Tale blocco è costituito da valori interi, risultanti dalla
% quantizzazione dei coefficienti DCT. Bisogna fornire in ingresso anche il
% valore di predizione del coefficiente DC

%% Zig-zag scan
coeffs = zigzagscan(blk);

%% DC Coding
dcPredErr = coeffs(1)-dc; % prediction
cat = ceil(log2(abs(dcPredErr)+1));
bits = catValCod(cat,dcPredErr);
fprintf('Codifica DC\nValore DC:%d\tPredittore:%d\nDC_P\tCat\tBits\n', coeffs(1), dc);
fprintf('%3d%7d\t%s\n------------\n\n',dcPredErr,cat,bits);

%% AC Coding
fprintf('Codifica AC\n#AC    Run    Cat    Value   Bits\n')
coeffs(1)=1; % Per evitare problemi quando DC = 0. Tanto DC è stato gia codificato
nzp = find(coeffs);
runs = diff(nzp)-1;
ACvalues = coeffs(nzp(2:end));
acCat = ceil(log2(abs(ACvalues)+1));
for k = 1:numel(ACvalues),
    RC = [runs(k), acCat(k)];
    codeword = AChuffTables(runs(k), acCat(k));
    
    if ACvalues(k) >0 
        valCod =  dec2bin(ACvalues(k),acCat(k));
    else 
        valCod =  97-(dec2bin(-ACvalues(k),acCat(k)));
    end
    fprintf('%3d    %3d    %3d    %3d     %s %s\n',k,RC,ACvalues(k),codeword, valCod );
    bits = [bits codeword valCod];
end
bits = [bits '1010'];
fprintf('EOB                          1010\n------------\n')
