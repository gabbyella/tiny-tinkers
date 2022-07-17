% Gabriella Heifetz
% Self Sufficient LED Design Project
% Preliminary Program
% 6/15/14

close all
clear
format compact

x=1;                    % set always positive value x
ht=100;                 % set dimensions of cell matrix         
wd=100;
t=.05;                    % set time between each generation (in seconds)

A= zeros(ht,wd);   % create cell matrix
N= zeros(ht,wd,8); % create neighbor matrix
C=A;                    % create neighbor count matrix
life=zeros(ht,wd,3); % initialize image matrix
Generation=1;           %initialize generation

%% SET INITIAL CONDITIONS FOR CELL CULTURE
A(50,:)=ones;

disp('Game of Life is now running. See figure!')
disp('Press ctrl+c to terminate program.')

while x==1  % causes game to run continuously (as long as x=0 at end is commented out)
%% NEIGHBOR EVALUATOR: 
 % Fills in 'neighbor array' N which contains all neighbors of A(i,j) 
 % starting with upper left going clockwise (non-existant neighbors, aka
 % neighbors of elements on the edges are treated at 0's). Also fills in C
 % which is the count of 'live' neighbor cells for each cell.
 for i=1:ht  
    for j=1:wd
        ip=i+1;
        im=i-1;
        jp=j+1;
        jm=j-1;
        if i==1 
            if j==1 % upper left corner
                N(i,j,:)=[0,0,0,A(i,jp),A(ip,jp),A(ip,j),0,0];
            elseif j==wd % upper right corner
                N(i,j,:)=[0,0,0,0,0,A(ip,j),A(ip,jm),A(i,jm)];
            else % top row
                N(i,j,:)=[0,0,0,A(i,jp),A(ip,jp),A(ip,j),A(ip,jm),A(i,jm)];
            end
        elseif i==ht
            if j==1 % lower left corner
                N(i,j,:)=[0,A(im,j),A(im,jp),A(i,jp),0,0,0,0];
            elseif j==wd % lower right corner
                N(i,j,:)=[A(im,jm),A(im,j),0,0,0,0,0,A(i,jm)];
            else % bottom row
                N(i,j,:)=[A(im,jm),A(im,j),A(im,jp),A(i,jp),0,0,0,A(i,jm)];
            end
        elseif i>1
            if j==1 % left column
                N(i,j,:)=[0,A(im,j),A(im,jp),A(i,jp),A(ip,jp),A(ip,j),0,0];
            elseif j==wd % right column
                N(i,j,:)=[A(im,jm),A(im,j),0,0,0,A(ip,j),A(ip,jm),A(i,jm)];
            elseif j>1 % middles
                N(i,j,:)=[A(im,jm),A(im,j),A(im,jp),A(i,jp),A(ip,jp),A(ip,j),A(ip,jm),A(i,jm)];  
            end
        end
        C(i,j)=sum(N(i,j,:));
    end
 end
%% PLOT IMAGE
 life(:,:,1)=A;     % change color of living cells by leaving lines uncommented   
 %life(:,:,2)=A;     % r=1  g=2  b=3  y=1,2  m=1,3  c=2,3  wh=1,2,3 
 life(:,:,3)=A;
 image(life)
 disp(sprintf('Generation %g', Generation));
 pause(t)

%% NEXT GENERATION FORMATION
for k=1:ht  
    for l=1:wd
        if A(k,l)==1        % in a living cell, if it has...
            if C(k,l)<2     % less than 2 living neighbors, it dies
                A(k,l)=0;
            elseif C(k,l)>3 % more than 3 living neighbors, it dies
                A(k,l)=0;
            end             % 2 or 3 living neighbors, it continues to live
        elseif A(k,l)==0    % in a dead cell, if it has...
            if C(k,l)==3    % exactly 3 living neighbors, becomes live
                A(k,l)=1;
            end             % otherwise, stays dead
        end
    end
end
Generation=Generation+1;
%x=0;
end