import ox

lexer = ox.make_lexer([
    ('EQUAL', r'='),
    ('STRING', r'\"'),
    ('TEXT', r'[\w*°*\?*\(*\)*\.*\,*\:*\-*]+'),
    ('OPEN_SECTION', r'\['),
    ('CLOSE_SECTION', r'\]'),
    ('OPEN_SUBSECTION', r'\[\['),
    ('CLOSE_SUBSECTION', r'\]\]'),
    ('OPEN_DATA', r'\{'),
    ('CLOSE_DATA', r'\}'),
    ('IGNORE', r'\s+'),
    ('COMMENT', r'\#'),
])

tokens_list = ['EQUAL',
               'STRING',
               'TEXT',
               'OPEN_SECTION',
               'CLOSE_SECTION',
               'OPEN_SUBSECTION',
               'CLOSE_SUBSECTION',
               'OPEN_DATA',
               'CLOSE_DATA',
               'IGNORE',
               'COMMENT']

all_body_ignore = lambda ignore, all_file: (all_file)
all_body= lambda left, right: (left, right)
open_close = lambda open, text, close: (text)
section = lambda open, text, close, end_line, body: (('section',text), body)
section_no_body = lambda open, text, close, end_line: (('section',text))
subsection = lambda open, text, close,end_line, body: (('subsection',text), body)
open_close_ignore = lambda open, ignoreopen, text, ignoreclose, close: (text)
open_close_data_ignore = lambda open_data, ignoreopen, text, ignoreclose, close_data: (('open_data',open_data),text,('close_data',close_data))
data_compound = lambda left, ignore, right:(left, right)
string_data = lambda left, data, right: (('open_string',left), data, ('close_string',right))
data_ignore = lambda left, ignore,right: (left, right)
data_comment = lambda hash_comment, comment: (('comment',hash_comment), comment)
data_comment_hash = lambda hash_comment: ('comment',hash_comment)
data= lambda left, right: (left, right)
attribute = lambda variable, equal, attribute, end_line: (variable,('attr', equal), attribute)
atom = lambda text: ('text',text)

parser = ox.make_parser([
    ('all_file : IGNORE all_file', all_body_ignore),
    ('all_file : comment IGNORE all_file', data_ignore),
    ('all_file : all_section', lambda x:x),
    ('all_section : all_section section', all_body),
    ('all_section : section', lambda x:x),
    ('section : OPEN_SECTION TEXT CLOSE_SECTION IGNORE body_section', section),
    ('section : OPEN_SECTION TEXT CLOSE_SECTION IGNORE', section_no_body),
    ('body_section : body_section subsection', all_body),
    ('body_section : subsection', lambda x:x),
    ('body_section : body', lambda x:x),
    ('subsection : OPEN_SUBSECTION TEXT CLOSE_SUBSECTION IGNORE body', subsection),
    ('body : body attribute', all_body),
    ('body : attribute', lambda x:x),
    ('attribute : comment IGNORE attribute', data_ignore),
    ('attribute : atom EQUAL data_compound IGNORE', attribute),
    ('data_compound : OPEN_DATA IGNORE data_ignore IGNORE CLOSE_DATA', open_close_data_ignore),
    ('data_ignore : data_ignore IGNORE data_compound', data_ignore),
    ('data_ignore : data_compound', lambda x:x),
    ('data_compound : STRING data STRING', string_data),
    ('data_compound : data', lambda x: x),
    ('comment : COMMENT data', data_comment),
    ('data : data atom', data),
    ('data : atom', lambda x: x),
    ('atom : TEXT', atom),
], tokens_list)


expr = """
	#Data from Viard et al. (1996) Microsatellite and the genetics of highly
	#selfing populations in the freshwater snail Bulinus truncatus. Genetics 142:1237-1247.
	#We thank Philippe Jarne and Frederique Viard for having kindly provided us with these data

    [Profile]
	Title="Microsatellite polymorphism in Bulinus truncatus"
		NbSamples=14
		DataType=MICROSAT
		GenotypicData=1
		GameticPhase=0
		MissingData="?"
		LocusSeparator=WHITESPACE

[Data]

	[[Samples]]
	#There are 4 loci  BT1 BT6 BT12 and BT13
	#The microsatellite alleles are expressed as the PCR fragment size

		SampleName="Bala"
		SampleSize=30
		SampleData={
       BT0BA1E1 17 		 184 116 258 280
                         184 116 258 280
       BT0BA2E2  1       184 116 258 276
                         184 116 258 276
       BT0BA4E4  4       184 116 258 284
                         184 116 258 284
     BT0BA13E13  4       184 116 262 280
                         184 116 262 280
     BT0BA16E16  1       184 116 262 288
                         184 116 262 288
     BT0BA22E22  2       184 116 262 284
                         184 116 262 284
     BT0BA28E28  1       186 116 258 280
                         186 116 258 280
		}
		SampleName="Mari Nord"
		SampleSize=29
		SampleData={
        BT0MN11 1        184 157 318 304
                         184 157 318 304
        BT0MN22 1        180 116 318 284
                         184 116 318 284
        BT0MN33 1        184 157 246 260
                         184 157 318 260
        BT0MN44 1        180 157 254 256
                         184 157 254 284
        BT0MN55 1        180 151 250 284
                         184 157 274 284
        BT0MN66 1        180 151 250 284
                         180 151 250 284
        BT0MN77 1        184 116 306 284
                         184 116 306 284
        BT0MN88 1        184 157 310 368
                         184 157 310 368
        BT0MN99 1        184 157 306 296
                         184 157 306 296
      BT0MN1010 1        184 116 318 260
                         184 116 318 260
      BT0MN1111 1        184 157 250 376
                         184 157 250 376
      BT0MN1212 1        180 116 254 288
                         180 116 254 288
      BT0MN1313 1        180 157 254 300
                         180 157 254 304
      BT0MN1514 1        184 116 306 260
                         184 157 306 368
      BT0MN1615 1        180 151 318 288
                         180 151 318 296
      BT0MN1716 1        184 151 250 348
                         184 151 250 348
      BT0MN1817 1        184 116 250 260
                         184 159 250 260
      BT0MN1918 1        180 116 310 260
                         180 116 310 260
      BT0MN2019 1        180 157 254 260
                         180 157 306 260
      BT0MN2120 1        180 151 250 260
                         180 151 310 288
      BT0MN2221 1        184 151 250 292
                         184 151 254 292
      BT0MN2322 1        184 157 314 256
                         184 157 314 256
      BT°MN2423 1        184 157 250 296
                         184 157 250 296
      BT0MN2524 1        184 157 250 288
                         184 157 250 368
      BT0MN2625 1        184 157 310 288
                         184 157 310 368
      BT0MN2726 1        180 157 314 368
                         180 157 314 368
      BT0MN2827 1        184 116 314 368
                         184 116 314 368
      BT0MN2928 1        184 157 306 260
                         184 157 306 260
      BT0MN3029 1        184 116 274 384
                         184 116 274 384
		}
		SampleName="Namaga PM"
		SampleSize=28
		SampleData={
       BT0Npm11 2        180 157 270 416
                         180 157 270 416
       BT0Npm22 1        176 143 242 296
                         176 143 242 296
       BT0Npm33 1        176 143 262 264
                         180 143 270 264
       BT0Npm44 1        180 157 278 420
                         180 157 278 420
       BT0Npm55 1        180 143 238 420
                         180 143 238 420
       BT0Npm66 1        180 157 262 396
                         180 157 262 396
       BT0Npm77 1        180 157 278 416
                         180 157 278 416
       BT0Npm88 1        180 143 250 416
                         180 143 250 416
       BT0Npm99 2        180 157 270 420
                         180 157 270 420
     BT0Npm1010 1        184 143 278 284
                         184 157 278 284
     BT0Npm1111 1        184 143 270 424
                         184 143 270 424
     BT0Npm1212 1        180 143 254 356
                         180 155 270 356
     BT0Npm1313 1        180 157 238 284
                         180 157 238 284
     BT0Npm1414 1        180 143 238 284
                         180 143 238 284
     BT0Npm1515 2        180 143 270 416
                         180 143 270 416
     BT0Npm1616 1        180 157 250 284
                         180 157 250 284
     BT0Npm1818 1        176 157 246 420
                         180 157 278 420
     BT0Npm2020 1        176 157 246 284
                         176 157 246 284
     BT0Npm2121 1        180 157 250 392
                         184 157 250 392
     BT0Npm2222 1        180 157 266 254
                         180 157 266 254
     BT0Npm2323 1        180 143 238 352
                         180 143 238 352
     BT0Npm2424 1        180 157 278 416
                         180 157 282 416
     BT0Npm2525 1        180 143 274 412
                         180 143 274 412
     BT0Npm2726 1        184 143 250 288
                         184 157 270 260
     BT0Npm2927 1        180 143 238 356
                         180 143 270 356
		}
		SampleName="Namaga B"
		SampleSize=23
		SampleData={
       BT0NG1A1 1        176 143 278 416
                         176 143 278 416
       BT0NG2A2 1        180 157 238 392
                         180 157 238 392
       BT0NG3A3 1        180 157 250 260
                         180 157 250 260
       BT0NG4A4 1        180 143 274 416
                         180 143 274 416
       BT0NG5A5 1        184 143 270 264
                         184 157 270 264
       BT0NG7A6 2        180 155 270 352
                         180 155 270 352
      BT0NG11A8 1        176 143 270 356
                         176 143 270 356
      BT0NG12A9 1        176 143 238 288
                         176 143 238 288
     BT0NG13A10 1        180 157 254 284
                         180 157 254 284
     BT0NG14A11 1        180 143 270 256
                         184 143 270 420
     BT0NG16A12 2        176 143 262 380
                         176 143 262 380
     BT0NG72E13 1        180 143 262 256
                         180 157 262 256
     BT0NG74E15 1        176 143 238 396
                         180 157 238 396
     BT0NG76E16 1        180 143 250 288
                         180 143 250 288
     BT0NG77E17 1        184 157 250 288
                         184 157 250 288
     BT0NG78E18 1        180 157 250 416
                         180 157 250 416
     BT0NG79E19 1        176 143 262 416
                         180 143 274 424
     BT0NG80E20 1        176 143 254 288
                         180 143 262 416
     BT0NG81E21 1        176 143 274 404
                         176 155 278 416
     BT0NG82E22 1        184 157 250 256
                         184 157 250 256
     BT0NG85E23 1        180 157 254 420
                         180 157 254 420
		}
		SampleName="Namaga W"
		SampleSize=37
		SampleData={
       BT0NW021 1        180 143 274 284
                         180 143 274 284
       BT0NW032 1        180 143 270 260
                         180 143 270 260
       BT0NW043 2        180 157 246 384
                         180 157 246 384
       BT0NW054 1        180 143 226 396
                         180 143 226 396
       BT0NW065 1        176 143 278 396
                         176 143 278 396
       BT0NW076 2        180 143 254 284
                         180 143 254 284
       BT0NW087 1        184 143 258 292
                         184 143 258 292
       BT0NW098 1        176 157 254 284
                         176 157 254 284
       BT0NW109 3        176 143 274 396
                         176 143 274 396
      BT0NW1110 3        184 157 270 376
                         184 157 270 376
      BT0NW1211 1        176 143 262 288
                         176 143 262 288
      BT0NW1413 1        180 143 258 292
                         180 143 258 292
      BT0NW1514 2        176 143 258 284
                         176 143 258 284
      BT0NW1716 1        176 143 262 284
                         176 143 262 284
      BT0NW1817 1        176 143 274 292
                         176 143 274 292
      BT0NW2019 1        176 143 270 408
                         176 143 270 408
      BT0NW2120 1        180 157 274 288
                         180 157 274 288
      BT0NW2221 1        180 157 270 396
                         180 157 270 396
      BT0NW2524 1        180 143 274 280
                         180 143 274 280
      BT0NW2625 5        176 143 258 280
                         176 143 258 280
      BT0NW2726 1        176 143 274 392
                         176 143 274 392
      BT0NW2827 2        180 143 254 280
                         180 143 254 280
      BT0NW3029 1        180 143 226 392
                         180 143 226 392
      BT0NW3433 1        180 157 274 280
                         180 157 274 280
      BT0NW3534 1        180 143 266 258
                         180 143 266 258
		}
		SampleName="Tera"
		SampleSize=36
		SampleData={
       BT0TEI11  2       184 161 238 344
                         184 161 238 344
       BT0TEI22 16       184 161 290 384
                         184 161 290 384
       BT0TEI33  2       184 161 294 380
                         184 161 294 380
       BT0TEI55  6       184 143 294 376
                         184 143 294 376
       BT0TEI99  1       184 143 294 384
                         184 143 294 384
     BT0TEI1010  1       184 143 290 384
                         184 143 290 384
     BT0TEI1212  1       180 143 290 384
                         180 143 290 384
     BT0TEI1313  1       184 161 290 388
                         184 161 290 384
     BT0TEI2222  2       184 161 298 384
                         184 161 298 384
     BT0TEI2929  2       184 161 294 384
                         184 161 294 384
     BT0TEI3030  1       184 149 238 384
                         184 149 238 384
     BT0TEI3535  1       184 161 294 376
                         184 161 298 376
		}
		SampleName="Boyze I"
		SampleSize=30
		SampleData={
       BT0BYI11 5        184 163 282 424
                         184 163 282 428
       BT0BYI22 1        184 163 278 424
                         184 163 286 428
       BT0BYI44 5        184 163 282 424
                         184 163 282 424
       BT0BYI55 11       184 163 278 424
                         184 163 278 424
     BT0BYI1515 1        184 163 282 428
                         184 163 282 428
     BT0BYI1616 5        184 163 278 428
                         184 163 278 428
     BT0BYI2424 1        184 163 282 424
                         184 163 286 424
     BT0BYI2727 1        184 163 282 424
                         184 163 278 424
		}
		SampleName="Boyze II"
		SampleSize=23
		SampleData={
      BT0BYII11 9        184 163 282 432
                         184 163 282 432
      BT0BYII66 2        184 163 282 424
                         184 163 282 428
      BT0BYII77 2        184 163 282 436
                         184 163 282 436
      BT0BYII99 5        184 163 286 428
                         184 163 286 428
     BT0BYII110 1        184 163 278 424
                         184 163 278 424
     BT0BYII114 3        184 163 282 428
                         184 163 282 428
     BT0BYII218 1        184 163 286 424
                         184 163 286 428
		}
		SampleName="Bouktra"
		SampleSize=21
		SampleData={
        BT0Bk11 5        184 165 214 264
                         184 165 214 264
        BT0Bk22 1        184 157 214 256
                         184 157 214 256
        BT0Bk44 1        184 165 394 268
                         184 165 394 268
        BT0Bk55 5        184 165 386 264
                         184 165 386 264
        BT0Bk88 1        184 165 214 260
                         184 165 214 264
      BT0Bk1010 3        184 165 206 264
                         184 165 206 264
      BT0Bk1111 1        184 157 242 256
                         184 157 242 256
      BT0Bk1414 1        184 157 242 276
                         184 157 242 276
      BT0Bk1616 1        184 165 242 264
                         184 165 242 264
      BT0Bk1717 1        184 165 290 264
                         184 165 290 264
      BT0Bk1919 1        184 165 398 276
                         184 165 398 276
		}
		SampleName="Foua"
		SampleSize=12
		SampleData={
         BT0F11 2        180 157 350 252
                         180 157 350 252
         BT0F22 2        180 157 214 252
                         180 157 214 252
         BT0F44 1        184 159 394 296
                         184 159 394 296
         BT0F55 1        180 157 358 248
                         180 157 358 248
         BT0F66 1        180 157 342 248
                         180 157 342 248
         BT0F77 1        180 165 390 272
                         180 165 390 272
         BT0F99 1        180 157 346 256
                         180 157 346 256
       BT0F1010 1        180 165 386 272
                         180 165 386 272
       BT0F1311 1        180 157 390 252
                         180 157 390 252
       BT0F1412 1        184 165 350 252
                         184 165 350 256
		}
		SampleName="Kobouri"
		SampleSize=16
		SampleData={
         BT0K11 4        184 155 286 336
                         184 155 286 336
         BT0K22 1        184 155 290 328
                         184 155 290 328
         BT0K33 2        184 155 286 328
                         184 155 286 328
         BT0K44 1        184 155 278 328
                         184 155 278 336
         BT0K55 5        184 155 286 332
                         184 155 286 332
         BT0K66 1        184 155 286 340
                         184 155 286 340
         BT0K77 1        184 155 282 328
                         184 155 282 336
         BT0K88 1        184 155 290 336
                         184 155 290 336
		}
		SampleName="Kokourou"
		SampleSize=31
		SampleData={
        BT0KO11 1        180 143 254 404
                         180 143 254 408
        BT0KO22 2        176 157 254 296
                         176 157 254 296
        BT0KO44 2        180 143 258 260
                         180 143 258 260
        BT0KO55 1        180 157 250 252
                         180 157 250 252
        BT0KO66 1        180 157 250 280
                         180 157 250 280
        BT0KO88 1        180 157 254 288
                         180 157 254 412
        BT0KO99 1        180 157 262 376
                         180 157 278 412
      BT0KO1010 1        180 143 250 288
                         180 157 250 380
      BT0KO1111 1        184 143 242 380
                         184 157 242 380
      BT0KO1212 1        180 157 262 280
                         180 157 262 280
      BT0KO1313 1        180 157 266 416
                         180 157 266 412
      BT0KO1414 1        180 143 254 256
                         180 143 254 256
      BT0KO1515 1        180 157 254 284
                         180 157 254 284
      BT0KO1616 1        180 143 250 256
                         180 143 250 256
      BT0KO1717 1        180 155 246 268
                         180 155 246 268
      BT0KO1818 1        180 143 246 260
                         180 155 250 280
      BT0KO1919 1        180 157 266 284
                         180 157 266 284
      BT0KO2020 1        184 157 262 412
                         184 157 262 412
      BT0KO2121 2        180 143 254 260
                         180 143 254 260
      BT0KO2323 1        184 155 246 268
                         184 155 246 268
      BT0KO2424 1        180 155 254 420
                         180 157 254 420
      BT0KO2525 3        184 155 282 332
                         184 155 282 332
      BT0KO2626 2        184 155 282 340
                         184 155 286 332
      BT0KO2727 1        184 155 282 340
                         184 155 286 340
      BT0KO2828 1        184 155 286 340
                         184 155 286 332
		}
		SampleName="Mada"
		SampleSize=33
		SampleData={
        BT0MD11 9        180 165 382 244
                         180 165 382 244
        BT0MD22 3        180 157 206 260
                         180 157 206 260
        BT0MD43 1        180 165 346 260
                         180 165 346 260
        BT0MD54 3        180 157 210 260
                         180 157 210 260
        BT0MD65 1        180 165 210 244
                         180 165 210 244
        BT0MD87 1        180 157 382 268
                         184 157 394 272
      BT0MD1311 1        180 165 382 248
                         180 165 382 248
      BT0MD1412 1        180 165 382 268
                         180 165 386 268
      BT0MD1816 1        180 165 342 260
                         180 165 342 260
      BT0MD2018 1        179 165 382 244
                         180 165 382 244
      BT0MD2119 1        180 165 378 248
                         180 165 378 248
      BT0MD2220 1        184 157 398 272
                         184 157 394 272
      BT0MD2321 1        180 165 346 244
                         180 165 346 244
      BT0MD2623 1        180 165 386 268
                         180 165 386 268
      BT0MD2724 2        184 165 330 272
                         184 165 330 272
      BT0MD2926 1        184 157 330 260
                         184 157 330 260
      BT0MD3128 1        179 165 346 244
                         180 165 346 244
      BT0MD3229 1        180 165 346 248
                         180 165 346 248
      BT0MD3330 1        180 157 206 244
                         180 157 206 244
      BT0MD3431 1        180 157 390 260
                         180 157 390 260
		}
		SampleName="Mari Sud"
		SampleSize=28
		SampleData={
        BT0M7A1 1        184 151 250 256
                         184 151 254 284
        BT0M8A2 1        184 116 250 260
                         184 151 278 288
        BT0M9A3 1        180 157 254 260
                         180 157 254 260
        BT0M1A4 1        179 116 318 368
                         179 116 318 368
        BT0M2A5 1        184 116 254 260
                         184 116 254 260
        BT0M3A6 1        184 157 310 256
                         184 157 310 256
        BT0M4A7 1        184 116 310 260
                         184 116 310 288
        BT0M5A8 1        184 116 250 260
                         184 116 250 284
        BT0M6A9 1        184 116 254 256
                         184 116 254 288
      BT0M64A10 2        184 157 250 296
                         184 157 250 296
      BTOM73A11 1        184 116 250 260
                         184 116 250 260
     BT0M104A12 1        180 157 278 288
                         184 157 278 288
     BT0M118A13 1        180 157 314 288
                         180 157 314 288
     BT0M119A14 2        184 157 314 260
                         184 157 314 260
     BT0M125E15 1        180 157 250 300
                         180 157 250 300
     BT0M127E16 1        180 116 250 368
                         180 116 250 368
     BT0M128E17 1        184 157 254 296
                         184 157 254 296
      BT0M11A19 1        180 116 254 260
                         184 116 314 260
      BT0M12A20 1        184 157 254 288
                         184 157 254 288
      BT0M13A21 1        180 157 310 256
                         180 157 310 280
      BT0M14A22 1        184 116 310 296
                         184 116 310 296
      BT0M15A23 1        184 116 250 260
                         184 116 250 300
     BT0M108A25 1        184 116 250 256
                         184 157 314 288
     BT0M109A26 1        184 116 310 260
                         184 116 310 260
     BT0M126E27 1        184 116 274 260
                         184 116 310 288
     BT0M140E28 1        180 157 250 256
                         184 157 314 368
		}


[[Structure]]

	StructureName = "Test"
	NbGroups = 3

	#Western Niger
	Group =  {
		"Bala"
		"Kobouri"
		"Kokourou"
		"Mari Sud"
		"Mari Nord"
		"Namaga PM"
		"Namaga B"
		"Namaga W"
		"Tera"
	}

	#Eastern Niger
	Group =  {
		"Bouktra"
		"Foua"
		"Mada"
	}

	#Central Niger
	Group =  {
		"Boyze I"
		"Boyze II"
	}
"""


def extract_head_type(head):
    if head is 'section':
        return 'section'
    elif head is 'subsection':
        return 'subsection'
    elif head is 'open_data':
        return 'open_data'
    elif head is 'close_data':
        return 'close_data'
    elif head is 'text':
        return 'text'
    elif head is 'comment':
        return 'comment'
    elif head is 'attr':
        return 'attr'
    elif head is 'open_string':
        return 'open_string'
    elif head is 'close_string':
        return 'close_string'
    else:
        return None


def eval(ast):
    head, *tail = ast
    string = ''
    if head:
        type_node = extract_head_type(head)
        if type_node:
            return type_node
        elif not type_node:
            type_node = eval(head)
            if type_node == 'comment':
                print(extract_comment(tail))
    if tail:
        eval(tail)


def extract_comment(data):
    head, *tail = data
    string = ''
    if head is 'text':
        return tail[0] + ' '
    elif head:
        string += extract_comment(head)
    if tail:
        string += extract_comment(tail)
    if not head and not tail:
        string += '\n'

    return string


def extract_data(data):
    head, *tail = data
    string = ''
    if head is 'text' or head is 'open_string' or head is 'close_string':
        return tail[0] + ' '
    elif head is 'close_data':
        string += '\n'
    else:
        if head:
            string += extract_data(head)
        if tail:
            string += extract_data(tail)

    return string


def extract_section(data):
    head, *tail = data
    string = ''
    if head is 'section' or head is 'open_string' or head is 'close_string':
        return tail[0] + ' '
    elif head is 'close_data':
        string += '\n'
    else:
        if head:
            string += extract_data(head)
        if tail:
            string += extract_data(tail)

    return string


tokens = lexer(expr)
ast = parser(tokens)
eval(ast)
