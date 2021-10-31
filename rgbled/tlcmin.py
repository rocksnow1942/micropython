s='length of value {} does not match COLORS_PER_PIXEL (= {})'
r='>H'
q='value[0] {} not in range: 0..1'
p='Riref {} not in range: 0.8kΩ..25kΩ'
o=None
n='WRITE_COMMAND'
m='OUTTMG'
l='EXTGCK'
k='TMGRST'
j='DSPRPT'
i='BLANK'
h='BCB'
g='BCG'
f='BCR'
Z='index {} out of range [0..{}]'
Y='Ioclmax {} not in range: 2mA..60mA'
V=1.0
U=len
T=list
S=float
R=isinstance
N=staticmethod
L=IndexError
I=0.0
H=range
G='length'
F='offset'
E='mask'
C=int
B=ValueError
import struct as M
from micropython import const as A
O=A(28)
D=A(3)
t=A(4)
W=A(12)
X=A(2)
u=A(6)
P=A(0)
v=A(21)
Q={f:{F:0,G:7,E:127},g:{F:7,G:7,E:127},h:{F:14,G:7,E:127}}
J=A(21)
w=A(5)
K={i:{F:0,G:1,E:1},j:{F:1,G:1,E:1},k:{F:2,G:1,E:1},l:{F:3,G:1,E:1},m:{F:4,G:1,E:1}}
a=A(26)
b={n:{F:0,G:6,E:63}}
c=A(37)
d=A(4)
class TLC:
	def __init__(A,spi,*,pixel_count=4):C=False;B=True;A._spi=spi;A.pixel_count=pixel_count;A.channel_count=A.pixel_count*D;A.chip_count=A.pixel_count//4;A._buffer=bytearray(O*A.chip_count);A.bcr=127;A.bcg=127;A.bcb=127;A.outtmg=B;A.extgck=C;A.tmgrst=B;A.dsprpt=B;A.blank=C;A._init_buffer();A._buffer_index_lookuptable=[];A._init_lookuptable()
	def _init_buffer(A):
		for B in H(A.chip_count):A.chip_set_BCData(B,bcr=A.bcr,bcg=A.bcg,bcb=A.bcb);A._chip_set_FunctionControl(B);A._chip_set_WriteCommand(B)
	def set_chipheader_bits_in_buffer(D,*,chip_index=0,part_bit_offset=0,field=o,value=0):
		K='>I';B=value;A=field
		if A is o:A={E:0,G:0,F:0}
		H=part_bit_offset+A[F];B&=A[E];B=B<<H;I=chip_index*O;C=M.unpack_from(K,D._buffer,I)[0];J=A[E]<<H;C&=~ J;C|=B;M.pack_into(K,D._buffer,I,C)
	def chip_set_BCData(A,chip_index,bcr=127,bcg=127,bcb=127):B=chip_index;A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=P,field=Q[f],value=bcr);A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=P,field=Q[g],value=bcg);A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=P,field=Q[h],value=bcb)
	def update_BCData(A):
		for B in H(A.chip_count):A.chip_set_BCData(B,bcr=A.bcr,bcg=A.bcg,bcb=A.bcb)
	def _chip_set_FunctionControl(A,chip_index):B=chip_index;A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=J,field=K[m],value=A.outtmg);A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=J,field=K[l],value=A.extgck);A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=J,field=K[k],value=A.tmgrst);A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=J,field=K[j],value=A.dsprpt);A.set_chipheader_bits_in_buffer(chip_index=B,part_bit_offset=J,field=K[i],value=A.blank)
	def update_fc(A):
		for B in H(A.chip_count):A._chip_set_FunctionControl(B)
	def _chip_set_WriteCommand(A,chip_index):A.set_chipheader_bits_in_buffer(chip_index=chip_index,part_bit_offset=a,field=b[n],value=c)
	def _init_lookuptable(B):
		for C in H(B.channel_count):A=O//X*(C//W)+C%W;A*=X;A+=d;B._buffer_index_lookuptable.append(A)
	def _write(A):A._spi.write(A._buffer)
	def show(A):A._write()
	@N
	def calculate_Ioclmax(*,Riref=2.48):
		A=Riref
		if not 0.8<=A<=24.8:raise B(p.format(A))
		D=1.21;C=41/A*D
		if not 2.0<=C<=60.0:raise B(Y.format(C))
		return C
	@N
	def calculate_Riref(*,Ioclmax=20):
		A=Ioclmax
		if not 2.0<=A<=60.0:raise B(Y.format(A))
		D=1.21;C=D/A*41
		if not 0.8<=C<=24.8:raise B(p.format(C))
		return C
	@N
	def calculate_BCData(*,Ioclmax=18,IoutR=17,IoutG=15,IoutB=9):
		F=IoutB;E=IoutG;D=IoutR;A=Ioclmax
		if not 2.0<=A<=60.0:raise B(Y.format(A))
		if not I<=D<=A:raise B('IoutR {} not in range: 2mA..{}mA'.format(D,A))
		if not I<=E<=A:raise B('IoutG {} not in range: 2mA..{}mA'.format(E,A))
		if not I<=F<=A:raise B('IoutB {} not in range: 2mA..{}mA'.format(F,A))
		G=C(D/A*127);H=C(E/A*127);J=C(F/A*127)
		if not 0<=G<=127:raise B('bcr {} not in range: 0..127'.format(G))
		if not 0<=H<=127:raise B('bcg {} not in range: 0..127'.format(H))
		if not 0<=J<=127:raise B('bcb {} not in range: 0..127'.format(J))
		return G,H,J
	@N
	def _convert_01_float_to_16bit_integer(value):
		A=value
		if not I<=A[0]<=V:raise B(q.format(A[0]))
		return C(A*65535)
	@classmethod
	def _convert_if_float(B,value):
		A=value
		if R(A,S):A=B._convert_01_float_to_16bit_integer(A)
		return A
	@N
	def _check_and_convert(value):
		A=value
		if R(A[0],S):
			if not I<=A[0]<=V:raise B(q.format(A[0]))
			A[0]=C(A[0]*65535)
		elif not 0<=A[0]<=65535:raise B('value[0] {} not in range: 0..65535'.format(A[0]))
		if R(A[1],S):
			if not I<=A[1]<=V:raise B('value[1] {} not in range: 0..1'.format(A[1]))
			A[1]=C(A[1]*65535)
		elif not 0<=A[1]<=65535:raise B('value[1] {} not in range: 0..65535'.format(A[1]))
		if R(A[2],S):
			if not I<=A[2]<=V:raise B('value[2] {} not in range: 0..1'.format(A[2]))
			A[2]=C(A[2]*65535)
		elif not 0<=A[2]<=65535:raise B('value[2] {} not in range: 0..65535'.format(A[2]))
	def _get_channel_16bit_value(A,channel_index):B=A._buffer_index_lookuptable[channel_index];return M.unpack_from(r,A._buffer,B)[0]
	def set_pixel_16bit_value(A,pixel_index,value_r,value_g,value_b):G=value_b;F=value_g;E=value_r;C=pixel_index*D;B=A._buffer_index_lookuptable[C+0];A._buffer[B+0]=G>>8&255;A._buffer[B+1]=G&255;B=A._buffer_index_lookuptable[C+1];A._buffer[B+0]=F>>8&255;A._buffer[B+1]=F&255;B=A._buffer_index_lookuptable[C+2];A._buffer[B+0]=E>>8&255;A._buffer[B+1]=E&255
	def set_pixel_float_value(A,pixel_index,value_r,value_g,value_b):G=value_b;F=value_g;E=value_r;E=C(E*65535);F=C(F*65535);G=C(G*65535);H=pixel_index*D;B=A._buffer_index_lookuptable[H+0];A._buffer[B+0]=G>>8&255;A._buffer[B+1]=G&255;B=A._buffer_index_lookuptable[H+1];A._buffer[B+0]=F>>8&255;A._buffer[B+1]=F&255;B=A._buffer_index_lookuptable[H+2];A._buffer[B+0]=E>>8&255;A._buffer[B+1]=E&255
	def set_pixel_16bit_color(A,pixel_index,color):B=color;B=T(B);E=pixel_index*D;C=A._buffer_index_lookuptable[E+0];A._buffer[C+0]=B[2]>>8&255;A._buffer[C+1]=B[2]&255;C=A._buffer_index_lookuptable[E+1];A._buffer[C+0]=B[1]>>8&255;A._buffer[C+1]=B[1]&255;C=A._buffer_index_lookuptable[E+2];A._buffer[C+0]=B[0]>>8&255;A._buffer[C+1]=B[0]&255
	def set_pixel_float_color(B,pixel_index,color):A=color;A=T(A);A[0]=C(A[0]*65535);A[1]=C(A[1]*65535);A[2]=C(A[2]*65535);F=pixel_index*D;E=B._buffer_index_lookuptable[F+0];B._buffer[E+0]=A[2]>>8&255;B._buffer[E+1]=A[2]&255;E=B._buffer_index_lookuptable[F+1];B._buffer[E+0]=A[1]>>8&255;B._buffer[E+1]=A[1]&255;E=B._buffer_index_lookuptable[F+2];B._buffer[E+0]=A[0]>>8&255;B._buffer[E+1]=A[0]&255
	def set_pixel(B,pixel_index,value):
		C=pixel_index;A=value
		if 0<=C<B.pixel_count:
			A=T(A)
			if U(A)!=D:raise L(s.format(U(A),D))
			B._check_and_convert(A);B.set_pixel_16bit_value(C,A[0],A[1],A[2])
		else:raise L(Z.format(C,B.pixel_count))
	def set_pixel_all_16bit_value(A,value_r,value_g,value_b):
		for B in H(A.pixel_count):A.set_pixel_16bit_value(B,value_r,value_g,value_b)
	def set_pixel_all(A,color):
		for B in H(A.pixel_count):A.set_pixel(B,color)
	def set_all_black(A):
		for B in H(A.pixel_count):A.set_pixel_16bit_value(B,0,0,0)
	def set_channel(C,channel_index,value):
		E=value;A=channel_index
		if 0<=A<C.channel_count:
			if not 0<=E<=65535:raise B('value {} not in range: 0..65535')
			F=A%D
			if F==0:A+=2
			elif F==2:A-=2
			G=C._buffer_index_lookuptable[A];M.pack_into(r,C._buffer,G,E)
		else:raise L('channel_index {} out of range (0..{})'.format(A,C.channel_count))
	def __len__(A):return A.pixel_count
	def __getitem__(A,key):
		B=key
		if 0<=B<A.pixel_count:C=B*D;return A._get_channel_16bit_value(C+0),A._get_channel_16bit_value(C+1),A._get_channel_16bit_value(C+2)
		raise L(Z.format(B,A.pixel_count))
	def __setitem__(B,key,value):
		C=key;A=value
		if 0<=C<B.pixel_count:
			A=T(A)
			if U(A)!=D:raise L(s.format(U(A),D))
			B._check_and_convert(A);B.set_pixel_16bit_value(C,A[0],A[1],A[2])
		else:raise L(Z.format(C,B.pixel_count))
	class _ChannelDirekt:
		def __init__(A,channel):A._channel=channel
		def __get__(A,obj,obj_type):return obj._get_channel_16bit_value(A._channel)
		def __set__(B,obj,value):A=value;assert 0<=A<=65535;obj.set_channel(B._channel,A)
	b0=_ChannelDirekt(0);g0=_ChannelDirekt(1);r0=_ChannelDirekt(2);b1=_ChannelDirekt(3);g1=_ChannelDirekt(4);r1=_ChannelDirekt(5);b2=_ChannelDirekt(6);g2=_ChannelDirekt(7);r2=_ChannelDirekt(8);b3=_ChannelDirekt(9);g3=_ChannelDirekt(10);r3=_ChannelDirekt(11)
class TLCA(TLC):
	def __init__(A,spi,pixel_count=4):super().__init__(spi,pixel_count=pixel_count)
	def set_pixel(A,pixel_index,value):super().set_pixel(pixel_index,value);A._write()
	def set_pixel_all(A,color):super().set_pixel_all(color);A._write()
	def set_all_black(A):super().set_all_black();A._write()
	def set_channel(A,channel_index,value):super().set_channel(channel_index,value);A._write()
	def __setitem__(A,key,value):super().__setitem__(key,value);A._write()
	class _ChannelDirektAutoShow:
		def __init__(A,channel):A._channel=channel
		def __get__(A,obj,obj_type):return obj._get_channel_16bit_value(A._channel)
		def __set__(B,obj,value):A=value;assert 0<=A<=65535;obj.set_channel(B._channel,A);obj._write()
	b0=_ChannelDirektAutoShow(0);g0=_ChannelDirektAutoShow(1);r0=_ChannelDirektAutoShow(2);b1=_ChannelDirektAutoShow(3);g1=_ChannelDirektAutoShow(4);r1=_ChannelDirektAutoShow(5);b2=_ChannelDirektAutoShow(6);g2=_ChannelDirektAutoShow(7);r2=_ChannelDirektAutoShow(8);b3=_ChannelDirektAutoShow(9);g3=_ChannelDirektAutoShow(10);r3=_ChannelDirektAutoShow(11)