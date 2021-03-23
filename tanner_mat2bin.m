clear,close all

load("./LDPC_matrix/format_mat/Tanner_R1-2_Z24_BG1.mat")

[M,N]=size(data)
fid = fopen("row_col_byCol_Tanner_R1-2_Z24_BG1.bin","w");
fwrite(fid,M,'int32');
fwrite(fid,N,'int32');
% for i =1:M
%     for j=1:N
%         fwrite(fid,data(i,j),'int32');
%     end
% end
fwrite(fid,data,'int32');
fclose("all");

fid=fopen("row_col_byCol_Tanner_R1-2_Z24_BG1.bin","r")
X = fread(fid,"int32");
M=X(1)
N=X(2)
Y = reshape(X(3:end),[M,N]);

fclose("all")
err=sum(Y~=data,'all')

%%
clear

load("./LDPC_matrix/format_mat/Tanner_R2-3_Z32_BG1.mat")

[M,N]=size(data)
fid = fopen("row_col_byCol_Tanner_R2-3_Z32_BG1.bin","w");
fwrite(fid,M,'int32');
fwrite(fid,N,'int32');
% for i =1:M
%     for j=1:N
%         fwrite(fid,data(i,j),'int32');
%     end
% end
fwrite(fid,data,'int32');
fclose("all");

fid=fopen("row_col_byCol_Tanner_R2-3_Z32_BG1.bin","r")
X = fread(fid,"int32");
M=X(1)
N=X(2)
Y = reshape(X(3:end),[M,N]);

fclose("all")
err=sum(Y~=data,'all')

