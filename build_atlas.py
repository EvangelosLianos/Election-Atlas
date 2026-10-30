import json, os, collections, openpyxl
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
base='/mnt/data/election_atlas'; raw=json.load(open('/mnt/data/NYStatewide_Nov24_ED_Consolidated_011125.geojson'))
counties={'Queens','Nassau','Suffolk'}
features={str(f['properties']['GEOID24']):f for f in raw['features'] if f['properties']['CountyName'] in counties and f.get('geometry')}
wb=openpyxl.load_workbook('/mnt/data/NY_2024StatewideResults-75a75e51.xlsx',read_only=True,data_only=True)
s=wb.active; it=iter(s.values); cols=next(it)
rows={}
for r in it:
 d=dict(zip(cols,r));
 if d['CountyName'] not in counties: continue
 k=str(d['GEOID24']);rows[k]=d
metrics=['Pres_HarrisTotal','Pres_TrumpTotal','Congress_DemTotal','Congress_RepTotal','Congress_ThirdTotal','USSen_GillibrandTotal','USSen_SapraiconeTotal','USSen_SareTotal','StateSen_DemTotal','StateSen_RepTotal','StateSen_ThirdTotal','Assembly_DemTotal','Assembly_RepTotal','Assembly_ThirdTotal','Prop1_Yes','Prop1_No']
line_fields=['Congress_D','Congress_R','Congress_C','Congress_W','Congress_CS','Congress_LR','Congress_Tru','Congress_WI']
allf=[];missing=[]; invalid=0
for k,f in features.items():
 r=rows.get(k)
 if not r:missing.append(k);continue
 p=f['properties']; g=shape(f['geometry']);
 if not g.is_valid: g=g.buffer(0);invalid+=1
 if g.is_empty: continue
 g=g.simplify(.00011,preserve_topology=True)
 props={'id':k,'county':p['CountyName'],'municipality':p.get('MuniName') or '', 'ed':p.get('EDName') or '', 'edid':str(p.get('EDID') or ''),'assembly':str(r.get('Assembly') or ''),'senate':str(r.get('Senate') or ''),'congress':str(r.get('Congress') or '')}
 for field in metrics+line_fields:
  v=r.get(field);props[field]=int(v) if isinstance(v,(float,int)) else 0
 allf.append({'type':'Feature','properties':props,'geometry':mapping(g)})
with open(base+'/data/districts.geojson','w') as h:json.dump({'type':'FeatureCollection','features':allf},h,separators=(',',':'))
print('boundaries',len(features),'results',len(rows),'joined',len(allf),'missing',len(missing),'invalid repaired',invalid,'bytes',os.path.getsize(base+'/data/districts.geojson'))
# AD overlay dissolved with simplified boundaries, split by county to avoid false adjacency
for layer,field in [('assembly','assembly'),('congress','congress')]:
 groups=collections.defaultdict(list)
 for f in allf:
  key=(f['properties']['county'],f['properties'][field]);
  if key[1]:groups[key].append(shape(f['geometry']))
 out=[]
 for (county,number),geoms in groups.items():
  geom=unary_union(geoms)
  if not geom.is_valid:geom=geom.buffer(0)
  geom=geom.simplify(.00018,preserve_topology=True)
  out.append({'type':'Feature','properties':{'county':county,'number':number},'geometry':mapping(geom)})
 with open(base+'/data/'+layer+'.geojson','w') as h:json.dump({'type':'FeatureCollection','features':out},h,separators=(',',':'))
 print(layer,len(out))
