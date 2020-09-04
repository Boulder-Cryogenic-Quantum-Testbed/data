% This file plots the power sweep, fits the TLS model, and plots that as
% well.

% O:\68707\ADR\data\20181012_W11_aSi_die1\2018_10_12_11_18_35_8p77_stitchedsweep

%% Input parameters:

tau0 = 0;
allscan = 1;
VNA_num = 0;
figyn = 0;
index = [];

T = 0.1;

%% Fit resonator

circlefit = [10800; 9010; 9132];
circlefreq = 7.409736;
Qc = 6124;
scans = [-60; -70; -80];
circlephotons = power2photons_hanger( circlefit, scans, -70, circlefreq );


%% Plot sweep
% Dave circle fit only

figure;

% loglog(psweep(:,1),1./psweep(:,2),'o')
loglog(circlephotons,1./circlefit,'o')
xlabel('$\langle n_{\textrm{ph}} \rangle$','Interpreter','latex');
ylabel('$\tan{\delta}$','Interpreter','latex');
set(gcf,'color','w')
set(gca, 'FontName', 'Arial')
set(gca,'Fontsize',9)
set(gca,'XMinorTick','on','YMinorTick','on')
hold on

%% Add fitting

f0 = circlefreq*10^9;

%calculate the Qi values for the fit line
h  = 6.626069934E-34;
kb = 1.38064852E-23;
tanh_hf0kbT = tanh(h*f0/(2*kb*T));
params0 = [3E3,1E-3,1,1]; % [Q_hp, Falpha, N_c, beta] guess
[paramsTLS, errorsTLS]= fitPowerSweep( circlephotons', circlefit', T, f0, params0 );
morephotons = logspace(log10(circlephotons(1)),log10(circlephotons(end)),100);
%paramsTLS(1) = 1.2174e+06;
%paramsTLS(4) = 0.35;
QiFit = localPowerTLSFit(paramsTLS,morephotons,tanh_hf0kbT);

plot(morephotons,1./QiFit)
legend('Data','Fit')

function f = localPowerTLSFit(params,photons,tanh_hf0kbT)
% Jonathan Burnett et all 2018, Noise and loss of superconducting aluminium resonators at single photon energies
% https://arxiv.org/pdf/1801.10204.pdf
% Here, f is the QTLS = 1/tandTLS
f = 1./((params(2)*tanh_hf0kbT)./(1.+photons./params(3)).^params(4) + 1/params(1));
end
