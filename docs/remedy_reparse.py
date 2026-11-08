import re,os,glob,html,json,collections
root=r"C:\Personal\Religion\Blogs\remedy_bible_corpus\_cache"
verses=[]; perbook=collections.defaultdict(lambda:[0,0]); red_verses=0; redpart=0
for p in glob.glob(os.path.join(root,"*.html")):
    h=open(p,encoding="utf-8",errors="replace").read()
    m=re.search(r"color=darkred><b>([^<]+)</b>.*?color=black>Chapter (\d+)</font>",h,re.S)
    if not m: continue
    book=m.group(1).strip(); ch=int(m.group(2))
    s=h.find("verseTxt"); e=h.find("chapterLinks",s)
    body=h[s:e]
    # tokens: verseNum or verse/red spans or <p></p>
    toks=re.findall(r"<span class=['\"](verseNum|verse|red)['\"]>(.*?)</span>|(<p></p>)",body,re.S)
    cur=None; segs=[]
    def flush():
        global red_verses
        if cur is None: return
        txt="".join(t for t,_ in segs).strip()
        txt=html.unescape(re.sub(r"<[^>]+>","",txt))
        isred=any(r for _,r in segs); hasplain=any(not r for _,r in segs)
        verses.append({"book":book,"chapter":ch,"verse":cur,"text":txt,"red":"all" if isred and not hasplain else ("part" if isred else "none")})
    for cls,txt,para in toks:
        if para: continue
        if cls=="verseNum":
            flush(); 
            try: cur=int(txt.strip())
            except: cur=None
            segs=[]
        else:
            segs.append((txt, cls=="red"))
    flush()
# coverage
books=collections.OrderedDict()
for v in verses:
    b=books.setdefault(v["book"],{"chapters":set(),"verses":0,"maxsum":collections.defaultdict(int),"red":0})
    b["chapters"].add(v["chapter"]); b["verses"]+=1
    b["maxsum"][v["chapter"]]=max(b["maxsum"][v["chapter"]],v["verse"] or 0)
    if v["red"]!="none": b["red"]+=1
tot=0;totmax=0
for bk,b in books.items():
    mx=sum(b["maxsum"].values()); tot+=b["verses"]; totmax+=mx
    print(f"{bk:16s} ch={len(b['chapters']):3d} verses={b['verses']:5d} sum(maxverse)={mx:5d} red={b['red']}")
print("TOTAL verses",tot,"sum of max verse numbers",totmax)
json.dump(verses,open(r"C:\Users\pwess\AppData\Local\Temp\claude\2770f3dc8a1463b0\3b7103ad-8681-49cb-af4d-6129a9f0477d\scratchpad\remedy_verses.json","w",encoding="utf-8"),ensure_ascii=False)
allt=" ".join(v["text"] for v in verses).lower()
print("words:",len(allt.split()))
terms={"wrath":r"\bwrath","anger/angry":r"\bang(er|ry)","fire":r"\bfire","law":r"\blaws?\b","design":r"\bdesign","justice":r"\bjustice","sacrific":r"\bsacrific","atone":r"\batone","judg":r"\bjudg","diagnos":r"\bdiagnos","fear":r"\bfear","sin":r"\bsin(s|ful|ner|ners)?\b","righteous":r"\brighteous","salvation":r"\bsalvation","heal":r"\bheal","remedy":r"\bremedy","infect":r"\binfect","selfish":r"\bselfish","trust":r"\btrust","faith":r"\bfaith","believe":r"\bbeliev","punish":r"\bpunish","terminal":r"\bterminal","character":r"\bcharacter","cure":r"\bcure","forgiv":r"\bforgiv","propitiat":r"propitiat","appease":r"\bappeas","hell":r"\bhell\b","grace":r"\bgrace","obey":r"\bobe[yd]","repent":r"\brepent","love":r"\blove","glory":r"\bglory","holy":r"\bholy","imposed":r"\bimposed","law of love":r"law of love","design law/protocol":r"design law|design protocol|design for life|design of love|designed","consequence":r"\bconsequence","let go / gave them up":r"gave them (up|over)|let (them|him|go) go|lets? go|no longer shield|withdr","treatment":r"\btreatment","physician":r"\bphysician","lies about God":r"lies? about god","methods and principles":r"methods and principles","coerc":r"\bcoerc","free(dom| will| choice)":r"\bfree (will|choice)|\bfreedom","individuality":r"\bindividualit","truth and love":r"truth and love","condemn":r"\bcondemn","legal":r"\blegal","penalty":r"\bpenalt","blood":r"\bblood","cross":r"\bcross\b","kingdom":r"\bkingdom","sabbath":r"\bsabbath","spirit":r"\bspirit\b","eternal (life|death)":r"eternal (life|death)","second death":r"second.{0,15}death"}
counts={k:len(re.findall(v,allt)) for k,v in terms.items()}
for k,c in sorted(counts.items(),key=lambda x:-x[1]): print(f"  {k:30s}{c}")
for term in ["fire","wrath","hell","atone","justice","propitiat|appeas","punish","diagnos","remedy"]:
    c=collections.Counter()
    for v in verses: c[v["book"]]+=len(re.findall(r"\b"+term,v["text"].lower()))
    print(term,"by book:",[(b,n) for b,n in c.most_common() if n])
