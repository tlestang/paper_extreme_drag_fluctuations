clf;
clear all;
close all;
Nt = 8000;
Nevents = 104;
dragMat = zeros(Nevents, Nt);
shearMat = zeros(Nevents, Nt);
ii=1;
allEvents = 1:104;
type2Events=[18 26 44 76 83 84 92 79];
inverseEvents=[9 39 55 65 100 87];
type1Events = allEvents(~ismember(allEvents,type2Events));
eventsMat = type2Events;
dragMat = zeros(length(eventsMat), Nt);
shearMat = zeros(length(eventsMat), Nt);
for i = 1:length(eventsMat)
  dirName = ['../instant_events/event_' num2str(eventsMat(i)) '_feb/'];
  fid = fopen([dirName 'data_force.datout'], 'r');
  f = fread(fid, [1 Inf], 'double');
  fclose(fid);
  fid = fopen([dirName 'vort_at_vortex.dat'], 'r');
  v = fread(fid, 1, 'double');
  fclose(fid);

  fid = fopen([dirName 'shearBot.dat'], 'r');
  shearBot = fread(fid, [1 Inf], 'double');
  fclose(fid);

  fid = fopen([dirName 'shearTop.dat'], 'r');
  shearTop = fread(fid, [1 Inf], 'double');
  fclose(fid);
  if(ismember(eventsMat(i),inverseEvents))
    if(max(shearBot(1:4000))>max(shearTop(1:4000)))
      shearMat(i,:) = shearTop;
    else
      shearMat(i,:) = shearBot;
    end
  else
    if(max(shearBot(1:4000))>max(shearTop(1:4000)))
      shearMat(i,:) = shearBot;
    else
      shearMat(i,:) = shearTop;
    end
  end
  dragMat(i,:) = f;
  M(i) = max(f);
end
avgDrag = mean(dragMat,1);
avgShear = mean(shearMat, 1);
 figure(1)
 hold on
 xlabel('Drag on obstacle', 'interpreter', 'latex', 'FontSize', 7)
 ylabel('Shear along top or bottom face', 'interpreter', 'latex', 'FontSize', 7)
 xlim([min(min(dragMat)) max(max(dragMat))]);
 ylim([min(min(shearMat)) max(max(shearMat))]);
 stride = floor(length(f)/100);
 for i=1:length(eventsMat)
   h(i) = plot(dragMat(i,3000:5000), shearMat(i,3000:5000), 'Color', [128/255 128/255 128/255], 'LineWidth', 0.5);
   %eventsMat(i)
   %pause()
 end
 plot(avgDrag, avgShear, 'b', 'LineWidth', 2)

 %% figure(1)
 %% hold on
 %%  stride = floor(length(f)/100);
 %%  for t=40:60
 %%    t
 %%    for i=1:length(eventsMat)
 %%      h(i) = plot(dragMat(i,1:t*stride), shearMat(i,1:t*stride), 'Color', 'k');
 %%      g(i) = plot(dragMat(i,t*stride), shearMat(i,t*stride), 'o', 'MarkerFaceColor', 'r', 'MarkerEdgeColor' , 'r', 'MarkerSize', 5);
 %%      title(['t= ' num2str(t)])
 %%    end
 %%    pause();
 %%    %print(figure(1), '-dpng', ['shear_asof_drag/phase_portrait_feb_' num2str(t) '.png'])
 %%    delete(h); delete(g);
 %%  end
 
