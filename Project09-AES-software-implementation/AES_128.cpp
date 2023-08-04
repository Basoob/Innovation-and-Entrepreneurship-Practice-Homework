#include<iostream>
#include<cstring>
#include<ctime>
using namespace std;


string MixColumn_mat[4][4] = {
	/**    0     1     2     3    */
	/*0*/{ "02", "03", "01", "01"},
	/*1*/{ "01", "02", "03", "01"},
	/*2*/{ "01", "01", "02", "03"},
	/*3*/{ "03", "01", "01", "02"} 
};//�л�Ͼ���
char Sbox[16][16][3] = {
	/****    0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f */
	/*0*/{ "63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76" },
	/*1*/{ "CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0" },
	/*2*/{ "B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15" },
	/*3*/{ "04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75" },
	/*4*/{ "09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84" },
	/*5*/{ "53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF" },
	/*6*/{ "D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8" },
	/*7*/{ "51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2" },
	/*8*/{ "CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73" },
	/*9*/{ "60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB" },
	/*a*/{ "E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79" },
	/*b*/{ "E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08" },
	/*c*/{ "BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A" },
	/*d*/{ "70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E" },
	/*e*/{ "E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF" },
	/*f*/{ "8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16" }
};// S��
string T_Xor_mat[4][10] = {
	/****   0     1     2     3     4     5     6     7     8     9    */
	/*0*/{ "01", "02", "04", "08", "10", "20", "40", "80","1B", "36" },
	/*1*/{ "00", "00", "00", "00", "00", "00", "00", "00","00", "00" },
	/*2*/{ "00", "00", "00", "00", "00", "00", "00", "00","00", "00" },
	/*3*/{ "00", "00", "00", "00", "00", "00", "00", "00","00", "00" }
};//T�����е��ֳ�������

//�л���г˷�����ĳ���'0001 1011'
string MixColumn_mul_02_const = "1B";

//Сд��ĸת��д��ĸ
string LowtoUpper(string low) {
	for (int i = 0; i < low.length(); i++) {
		if (low[i] >= 'a' && low[i] <= 'z') {
			low[i] -= 32;
		}
	}
	return low;
}
//������תʮ������
string BintoHex(string Bin) {
	string Hex = "";
	for (int i = 0; i < Bin.length() / 4; i++) {
		int num = (Bin[4 * i] - '0') * 8 + (Bin[4 * i + 1] - '0') * 4 + (Bin[4 * i + 2] - '0') * 2 + (Bin[4 * i + 3] - '0');
		if (0 <= num && num <= 9) Hex += (num + '0');
		else if (num == 10) Hex += "A";
		else if (num == 11) Hex += "B";
		else if (num == 12) Hex += "C";
		else if (num == 13) Hex += "D";
		else if (num == 14) Hex += "E";
		else Hex += "F";
	}
	return Hex;
}
//ʮ������ת������
string HextoBin(string Hex) {
	string Bin = "";
	for (int i = 0; i < Hex.length(); i++) {
		if (Hex[i] == '0') Bin += "0000";
		else if (Hex[i] == '1') Bin += "0001";
		else if (Hex[i] == '2') Bin += "0010";
		else if (Hex[i] == '3') Bin += "0011";
		else if (Hex[i] == '4') Bin += "0100";
		else if (Hex[i] == '5') Bin += "0101";
		else if (Hex[i] == '6') Bin += "0110";
		else if (Hex[i] == '7') Bin += "0111";
		else if (Hex[i] == '8') Bin += "1000";
		else if (Hex[i] == '9') Bin += "1001";
		else if (Hex[i] == 'A') Bin += "1010";
		else if (Hex[i] == 'B') Bin += "1011";
		else if (Hex[i] == 'C') Bin += "1100";
		else if (Hex[i] == 'D') Bin += "1101";
		else if (Hex[i] == 'E') Bin += "1110";
		else Bin += "1111";
	}
	return Bin;
}

//ʮ�������ַ�ת10��������,����ʮ������Ϊ��д��ĸ
int HextoDec(char Hex) {
	if (Hex >= '0' && Hex <= '9')
		return Hex - '0';
	else
		return Hex - 55;
}

//ʮ����תʮ������
string DectoHex(int n)
{
	int  x;
	string s;
	char c;
	while (n != 0) {
		x = n % 16;
		if (x < 10) {
			c = x + '0';
		}
		else {
			c = x + 'A' - 10;
		}
		s = c + s;
		n = n / 16;
	}
	if (s == "") {
		return "00";
	}
	else {
		return s;
	}
}
//�����ȳ���ʮ��������������򣬷���ʮ�����Ƶ������
string HexXor(string a, string b) {
	string A = HextoBin(a);
	string B = HextoBin(b);
	string x(A.length(), '0');
	for (int i = 0; i < A.length(); i++) {
		x[i] = (A[i] - '0') ^ (B[i] - '0') + '0';
	}
	return BintoHex(x);
}

void create_key(string a,string* m)
{
	for (int i = 0; i < size(a); i++)
	{
		m[i] = DectoHex(int(a[i]));
	}
	for (int i = size(a); i < 16; i++)
	{
		m[i] = "00";
	}
	
}
//��������еĸ���Ԫ��
void show_arr(string* m,int len)
{
	for (int i = 0; i < len; i++)
	{
		cout << m[i] << ' ';
	}
}
//��m[16]ת��Ϊm[4][4]
void transfer(string m_[16], string m[4][4])
{
	int n = 0;
	for (int j = 0; j < 4; j++)
	{
		for (int i = 0; i < 4; i++)
		{
			m[i][j] = m_[n];
			n++;
		}
	}
}
//���4x4�����еĸ���Ԫ��
void show_arr4(string m[4][4])
{
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			cout << m[i][j] << ' ';
		}
		cout << endl;
	}
	cout << endl;
}
//���4x8�����еĸ���Ԫ��
void show_arr4_11(string m[4][8])
{
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 8; j++)
		{
			cout << m[i][j] << ' ';
		}
		cout << endl;
	}
	cout << endl;
}
//�ֽڴ���
void SubBytes(string m[4][4])
{
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			m[i][j] = Sbox[HextoDec(m[i][j][0])][HextoDec(m[i][j][1])];  //�ֽڴ���(SubBytes)
		}
	}
}
//����λ
void ShiftRows(string m[4][4])
{
	string m_[4][4];//����m
	for (int i =0; i < 4; i++) 
	{
		for (int j = 0; j < 4; j++)
		{
			m_[i][j] = m[i][j];
		}
	}
	for (int i = 1; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			m[i][j] = m_[i][(j+i)%4];
		}
	}
}
string MixColumn_mul_02(string b)//8bit����������,���������
{
	string s;
	s = b;
	switch(b[0]-'0')//�ж���λΪ0����1
	{
		case 0:
			s.erase(s.begin());
			s.push_back('0');
			break;
		case 1:
			s.erase(s.begin());
			s.push_back('0');
			s = HexXor(BintoHex(s),MixColumn_mul_02_const);
			s = HextoBin(s);
			break;
	}
	return s;
}
//�л���еĳ˷�
string MixColumn_mul(string a, string b)//16�������룬2�������
{
	string A = HextoBin(a);
	string B = HextoBin(b);
	int flag = HextoDec(a[1]);
	string s;
	//cout << flag;
	switch (flag) 
	{
		case 1:
			s = B;
			break;
		case 2:
			s = MixColumn_mul_02(B);
			break;
		case 3:
			s = MixColumn_mul_02(B);
			s= HexXor(BintoHex(s),b);
			s = HextoBin(s);
			break;
	}
	return s;
}
//�л�� 
void MixColumn(string m_MC[4][4], string m[4][4])
{
	
	string s="00";
	string s_part;
	//cout << MixColumn_mat[0][0] << " " << m[0][0] << endl;
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			for (int k = 0;k < 4;k++)
			{
				s_part = MixColumn_mul(MixColumn_mat[i][k], m[k][j]);
				//cout << s_part << " ";
				s= HexXor(BintoHex(s_part), s);
			}
			//cout << s;
			m_MC[i][j] = s;
			//cout << endl;
			s = "00";

			s_part = "00";
		}
	}
}
//T�����е���ѭ��
void T_shiftwords(string key_extend[4][8], string T_result[4], int j)
{
	string tmp;
	tmp = key_extend[0][j];
	for (int i = 0;i < 3;i++)
	{
		T_result[i] = key_extend[i + 1][j];
	}
	T_result[3] = tmp;
}
//T�����е��ֽڴ���
void SubBytes(string m[4][8], string T_result[4], int j)
{
		for (int i = 0; i < 4; i++)
		{
			T_result[i] = Sbox[HextoDec(T_result[i][0])][HextoDec(T_result[i][1])];  //�ֽڴ���(SubBytes)
		}
}
//T�����е���򣬷���ʮ�����Ƶ������
void HexXor(string key_extend[4][8], string T_result[4], int j, int count)
{
	for (int i = 0;i < 4;i++)
	{
		T_result[i] = HexXor(T_result[i], T_Xor_mat[i][count]);
	}
}
//ģ4��Ϊ0ʱ����Կ��չ�����
void HexXor(string key_extend[4][8], int j)
{
	for (int i = 0;i < 4;i++)
	{
		key_extend[i][j] = HexXor(key_extend[i][j - 1], key_extend[i][j - 4]);
	}
}
//ģ4Ϊ0ʱ����Կ��չ�е����
void HexXor(string key_extend[4][8], string T_result[4], int j)
{
	for (int i = 0;i < 4;i++)
	{
		T_result[i] = HexXor(T_result[i], key_extend[i][j - 4]);
	}
}
//����Կ��չ��T����
void key_extend_T(string key_extend[4][8], string T_result[4], int j, int count)//jΪ���±꣬countΪ����
{
	T_shiftwords(key_extend, T_result, j);
	SubBytes(key_extend, T_result, j);
	HexXor(key_extend, T_result, j, count);
}

//����Կ��չ
void key_extend(string key_extend[4][8],string key[4][4],int count)
{
	string T_result[4];
	for (int j = 0;j < 8;j++)
	{
		if (j < 4)//�������е���Կ
		{
			for (int i = 0;i < 4;i++)
			{
				key_extend[i][j] = key[i][j];
			}
			continue;
		}
		if (j % 4 != 0)
		{
			HexXor(key_extend, j);
			continue;
		}
		else
		{
			key_extend_T(key_extend, T_result, j - 1, count);//T����
			HexXor(key_extend, T_result, j);
			for (int i = 0;i < 4;i++)//�����д����չ��Կ����
			{
				key_extend[i][j] = T_result[i];
			}
			continue;
		}
			
	}
}
//�ֺ���������ǰ9�ּ���
void Round(string m[4][4], string key_ex[4][8], string key[4][4],int count)
{
	//SubBytes(m);
	ShiftRows(m);
	string m_MC[4][4];
	MixColumn(m_MC, m);
	key_extend(key_ex, key,count);
	for (int l = 0; l < 4; l++)
	{
		for (int n = 0; n < 4; n++)
		{
			key[l][n] = key_ex[l][n + 4];
			//m[l][n] = HexXor(m[l][n], key[l][n]);
			m[l][n] = HexXor(m_MC[l][n], key[l][n]);
		}
	}
}
//�ֺ������������һ�ּ���
void Final_Round(string m[4][4], string key_ex[4][8], string key[4][4])
{
	SubBytes(m);
	ShiftRows(m);
	key_extend(key_ex, key, 9);
	for (int l = 0; l < 4; l++)
	{
		for (int n = 0; n < 4; n++)
		{
			key[l][n] = key_ex[l][n + 4];
			m[l][n] = HexXor(m[l][n], key[l][n]);
		}
	}
}


int main()
{
	clock_t startTime, endTime;
	string  m_[16],key_[16];//�����Լ���Կ����ʮ������������ʽ�洢
	string a;
	cout << "������ѧ�ţ�";
	cin >> a;//����ѧ��
	create_key(a, m_);//��0
	create_key(a, key_);
	for (int i = 0; i < 16; i++)
	{
		m_[i] = HexXor(m_[i], key_[i]);
	}

	string m[4][4], key[4][4],key_ex[4][8];//ת����ʽ
	/*ע�����з�ʽΪ��
	   0 4  8 12
	   1 5  9 13
	   2 6 10 14
       3 7 11 15*/
	transfer(m_, m);
	transfer(key_, key);
	cout << "���ܺ������Ϊ��" << endl;
	show_arr4(m);
	string text_m[10][2][4][4];
	for (int i = 0; i < 10; i++)
	{
		for (int x = 0; x < 2; x++)
		{
			for (int l = 0; l < 4; l++)
			{
				for (int k = 0; k < 4; k++)
				{
					if (l == 0 && k == 0)
					{
						text_m[i][x][l][k] = DectoHex(x);
						if (x != 0)
							text_m[i][x][l][k].insert(1, "0");
					}
					else
					{
						text_m[i][x][l][k] = DectoHex(i+1);
						text_m[i][x][l][k].insert(1, "0");
					}
				}
			}
			show_arr4(text_m[i][x]);
		}
		
	}
	show_arr4(key);
	cout << "10�����������ɣ��������м���" << endl;
	startTime = clock();
	for (int j = 0; j < 10; j++)
	{
		for (int x = 0; x < 2; x++)
		{
			for (int i = 0; i < 2; i++)
			{
				Round(text_m[j][x], key_ex, key, i);
			}
		}
		
	}
	for (int j = 0; j < 10; j++)
	{
		for (int x = 0; x < 2; x++)
		{
			show_arr4(text_m[j][x]);
		}
	}
	endTime = clock();
	cout << "���ܽ���������ʱ��" << endTime - startTime << "ms" << endl;
	double avertime = (endTime - startTime) / 100;
	cout << "һ������Կƽ����ʱ��" << avertime << "ms";
	return 0;
}
//01100011 11000110