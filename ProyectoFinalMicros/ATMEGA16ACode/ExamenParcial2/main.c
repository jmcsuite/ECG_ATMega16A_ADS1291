/*
 * PrimerParcial.c
 *
 * Created: 01/03/2022 09:13:45 a. m.
 * Author : jmcsu
 */ 

#define F_CPU 8000000
#define BAUD 9600
#define MYUBRR F_CPU/16/BAUD-1
#define INT2_vect _VECTOR(18)
#define ADC_INT _VECTOR(14)
#define INT0_vect _VECTOR(19)
#define PORTTECLADO PORTC
#define PINTECLADO PINC
#define DDRTECLADO DDRC
#define PORTLCD PORTC
#define PINLCD PINC
#define DDRLCD DDRC
#define RS 4 
#define RW 5
#define E 6
#define BF 3 
#define LCD_Cmd_Clear 0b00000001 //limpiar lcd
#define LCD_Cmd_Home 0b00000010 // puntero al inicio
#define LCD_Cmd_Func2Lin 0b00101000 // init 4 bits 2 lineas
#define LCD_Cmd_Off	0b00001000 // apagar lcd
#define LCD_Cmd_ModeDnS	 0b00000110		// entry mode (ir hacia la derecha, y no recorrer caracteres )
#define LCD_Cmd_OnsCsB	0b00001100 // prender lcd (no mostrar cursor)
#define LCD_blink_cursor 0b00001111 // mostrar cursor parpadeante y lcd;
#define TIMER0_COMP_vect _VECTOR(19)

#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>
#include <avr/interrupt.h>

uint8_t cero_en_bit(volatile uint8_t *LUGAR, uint8_t BIT){
	return (!(*LUGAR&(1<<BIT)));
}

uint8_t uno_en_bit(volatile uint8_t *LUGAR, uint8_t BIT){
	return (*LUGAR&(1<<BIT));
}
void saca_uno(volatile uint8_t *LUGAR, uint8_t BIT){
	*LUGAR=*LUGAR|(1<<BIT);
}

void saca_cero(volatile uint8_t *LUGAR, uint8_t BIT){
	*LUGAR=*LUGAR&~(1<<BIT);
}

// Empieza mi codigo xd

void busy_flag(void){
	DDRLCD &= 0b11110000; // Setupear como Entrada los puertos DB7... DB0;
	saca_cero(&PORTLCD, RS); // instruccion
	saca_uno(&PORTLCD, RW); // Lectura
	while(1){ // mientras que el flag del bus sea 0
		saca_uno(&PORTLCD, E); // enable
		_delay_ms(10);
		saca_cero(&PORTLCD, E); // disable
		if(uno_en_bit(&PINLCD, BF)) {break;}
		_delay_us(10);
		saca_uno(&PORTLCD, E); // enable
		_delay_ms(10);
		saca_cero(&PORTLCD, E); // disable
		_delay_us(10);
	}
	_delay_us(10);
	saca_uno(&PORTLCD, E); // enable
	_delay_ms(10);
	saca_cero(&PORTLCD, E); // disable
	_delay_us(10);
	// listo
	saca_cero(&PORTLCD, RS); // instruccion
	saca_cero(&PORTLCD, RW); // Escribit;
	// setupear puertos para escribir
	DDRLCD |= (15 >> 0);
}

void LCD_CMD_4BIT(uint8_t x){
	PORTLCD = x;
	
	saca_cero(&PORTLCD, RS); // instruccion
	saca_cero(&PORTLCD, RW); // Escribir
	saca_uno(&PORTLCD, E); // Enable
	_delay_ms(10);
	saca_cero(&PORTLCD, E); // disable
	busy_flag();
}

void LCD_CMD_8BIT(uint8_t x){
	PORTLCD = (x >> 4);
	saca_cero(&PORTLCD, RS); // instruccion
	saca_cero(&PORTLCD, RW); // Escribir
	saca_uno(&PORTLCD, E); // Enable
	_delay_ms(10);
	saca_cero(&PORTLCD, E); // disable
	
	PORTLCD = 0b00001111&x;
	saca_cero(&PORTLCD, RS); // instruccion
	saca_cero(&PORTLCD, RW); // Escribir
	saca_uno(&PORTLCD, E); // Enable
	_delay_ms(10);
	saca_cero(&PORTLCD, E); // disable
	
	busy_flag();
}
uint8_t cc = 0;
void LCD_DATO_8bit(uint8_t x){
	    cc++;
		PORTLCD = (x >> 4);
		saca_uno(&PORTLCD, RS); // dato
		saca_cero(&PORTLCD, RW); // Escribir
		saca_uno(&PORTLCD, E); // Enable
		_delay_ms(10);
		saca_cero(&PORTLCD, E); // disable
		
		PORTLCD = 0b00001111&x;
		saca_uno(&PORTLCD, RS); // dato
		saca_cero(&PORTLCD, RW); // Escribir
		saca_uno(&PORTLCD, E); // Enable
		_delay_ms(10);
		saca_cero(&PORTLCD, E); // disable
		
		busy_flag();
}

void LCD_WR_string(volatile char *s){
	char c;
	
	
	while((c=*s++)){
		if(cc == 36) return;
		if(c == '\n'){
			LCD_CMD_8BIT(0b11000000);
			cc = 16;
			continue;
		}else if(cc == 16){
			LCD_CMD_8BIT(0b11000000);
		}
		LCD_DATO_8bit(c);
		
	}
}

void inicializacion_lcd(){
	DDRLCD |= (15 >> 0);
	DDRLCD |= (1 << RS) | (1 << RW) | (1 << E); // setupear como salida los puertos 
	// inicializar el lcd obligatorio
	_delay_ms(16);
	LCD_CMD_4BIT(0b00000011);
	_delay_ms(4.2);
	LCD_CMD_4BIT(0b00000011);
	_delay_us(100);
	LCD_CMD_4BIT(0b00000011);
	_delay_us(100);
	LCD_CMD_4BIT(0b00000010);
	_delay_us(100);
	//Full LCD INIT
	LCD_CMD_8BIT(LCD_Cmd_Func2Lin); //4 Bits, n?mero de l?neas y tipo de letra
	LCD_CMD_8BIT(LCD_Cmd_Off); //apaga el display
	LCD_CMD_8BIT(LCD_Cmd_Clear); //limpia el display
	LCD_CMD_8BIT(LCD_Cmd_ModeDnS); //Entry mode set ID S
	LCD_CMD_8BIT(LCD_Cmd_OnsCsB); //Enciende el display
	
}

void LCD_numero(uint8_t x){
	uint8_t mien = x%10;
	x /= 10;
	if(x > 0) LCD_numero(x);
	LCD_DATO_8bit(mien + '0');
}

int8_t input(int8_t i, int8_t j){
	switch(i){
		case 0:
		switch(j){
			case 4:
			//on
			return 11;
			break;
			case 5:
			// uno
			return 1;
			break;
			case 6:
			// 4
			return 4;
			break;
			case 7:
			// 7
			return 7;
			break;
		}
		break;
		case 1:
		switch(j){
			case 4:
			//cero
			return 0;
			break;
			case 5:
			// 2
			return 2;
			break;
			case 6:
			// 5
			return 5;
			break;
			case 7:
			// 8
			return 8;
			break;
		}
		break;
		case 2:
		switch(j){
			case 4:
			//igual
			return 11;
			break;
			case 5:
			// 3
			return 3;
			break;
			case 6:
			// 6
			return 6;
			break;
			case 7:
			// 9
			return 9;
			break;
		}
		break;
		case 3:
		switch(j){
			case 4:
			//+
			return 11;
			break;
			case 5:
			// -
			return 11;
			break;
			case 6:
			// por
			return 11;
			break;
			case 7:
			// entre
			return 11;
			break;
		}
		break;
	}
	return 12;
}

int8_t teclado(){
	
	PORTTECLADO = 0b11110000;
	while((~PINTECLADO)&(1<<4) || (~PINTECLADO)&(1<<5) || (~PINTECLADO)&(1<<6) || (~PINTECLADO)&(1<<7) ) {}
	
	while(1){
		PORTTECLADO = 0b11111111;
		for(int8_t i = 0; i < 4; i++){
			PORTTECLADO = ~((~PORTTECLADO)|(1<<i));
			for(int8_t j = 4; j < 8; j++){
				if((~PINTECLADO)&(1<<j)){
					_delay_ms(50);
					return input(i, j); 
					
					while((~PINTECLADO)&(1<<j)) {}
					
				}
			}
			PORTTECLADO = PORTTECLADO|(1<<i);
		}
	} 
}

void clear_home_counter(void){
	LCD_CMD_8BIT(LCD_Cmd_Clear);
	LCD_CMD_8BIT(0b10000000);
	cc = 0;
}

void EEPROM_WRITE(uint16_t dir, uint8_t dat){
	while (uno_en_bit(&EECR, EEWE));
	EEAR = dir;
	EEDR = dat;
	//cli(); //Comentar si no utilizamos interrupcioes
	EECR |= (1<<EEMWE);
	EECR |= (1<<EEWE);
	//sei();
}

uint8_t EEPROM_READ(uint16_t dir){
	while (uno_en_bit(&EECR, EEWE));
	EEAR = dir;
	EECR |= (1<<EERE);
	return EEDR;
}





ISR(_VECTOR(19)){
	//timer overflow comp
}
volatile int estado, lugar;
ISR(_VECTOR(14)){ //adc overflow
	
	if(estado == 0){
		uint8_t lectura = ADCH;
		EEPROM_WRITE(lugar,lectura);
		lugar++;
	}
	if(lugar == 512){
		TCCR0 = 0;
		clear_home_counter();
		LCD_WR_string("EEPROM LLENO");
	}
}


void USART_Init (uint8_t ubrr)
{
	DDRD |= (1<<1);        //TX de salida (D1) y RX de entrada (D0)
	UBRRH = (uint8_t) (ubrr>>8);
	UBRRL = (uint8_t) (ubrr);
	UCSRB = (1<<RXEN)|(1<<TXEN)|(1<<RXCIE);
	//habilitErecepción, transmisión e interrupción de la recepción
	UCSRC = (1<<URSEL)|(1<<UCSZ1)|(1<<UCSZ0)|(0<<USBS);
	//paquetes de 8 bits, con 1 bits de parada, sin paridad
}
void SendByte( char data ){
	while ( !( UCSRA &(1 << UDRE)) );
	UDR = data;
}
volatile char cereal;
volatile int8_t listo_serial;
ISR(USART_RXC_vect)
{
	
	uint8_t dato = UDR;
	cereal = dato;
	listo_serial = 1;
}

uint16_t lectura_adc(){
	saca_uno(&ADCSRA, ADSC);
	while(uno_en_bit(&ADCSRA, ADSC)){
	}
	uint16_t a2 = ADCH;
	
	double unidad_adc = 0.01960784;
	if(a2 < 255) a2++;
	a2 = (double) a2 * unidad_adc;
	return a2;
	
}


void SPI_INIT_MASTER(){
	SPCR = 0;
	// MOSI, SCK como salidas, MISO como entrada
	DDRB = (1<<5) | (1<<7) | (1 << 4) ; // MOSI 5  SCK 7  MISO 6  SS 4
	// Configurar SPCR, si hiciera falta también SPSR (para interrupciones o velocidad).
	SPCR = (1 << SPE) | (1 << MSTR) | (1<< SPR1) | (1<< SPR0); // Enable, Master, 128 Fosc
	// Lectura de DRDYVB
	DDRA = 0;
	PORTA = 0b11111111;
	PORTB |= (1<<4);
}

uint8_t SPI_TRANSMIT(uint8_t data){
	// SS = 0;
	PORTB &= ~(1<<4);
	// Escribir el dato en SPDR
	SPDR = data;
	// Esperar hasta que el bit SPIF se tenga un 1 (para garantizar que terminEla transmisión)
	while( !( SPSR &  (1<<SPIF)) ){}
	// Regresar el bit del esclavo a 1.
	PORTB |= (1<<4);
	return SPDR;
}

uint8_t Instruction_Write(uint8_t dir, uint8_t data){
	// SS = 1;
	dir &= ~(1<<7);
	PORTB &= ~(1<<4);
	SPDR = dir;
	while( !( SPSR &  (1<<SPIF)) ){}
	SPDR = data;
	while( !( SPSR &  (1<<SPIF)) ){}
	// ss
	PORTB |= (1<<4);
	return SPDR;
}
uint8_t read[6];



uint8_t ReadChannel(uint8_t dir){
	PORTB &= ~(1<<4);
	dir |= 0x80;
	char buffer;
	SPDR = dir;
	while( !( SPSR &  (1<<SPIF)) ) {}
	buffer = SPDR;
	SPDR = 0;
	while( !( SPSR &  (1<<SPIF)) ) { }
	uint8_t ans = SPDR;
	
	PORTB |= (1<<4);
	return ans;
}

void ReadChip(uint8_t* read){
	read[0] = ReadChannel(0x30); // status channels y alarmb
	read[1] = ReadChannel(0x1A); // info channel1
	read[2] = ReadChannel(0x19); // alarm status
	read[3] = ReadChannel(0x37);
	read[4] = ReadChannel(0x38);
	read[5] = ReadChannel(0x39);
	return;
}

void InicializarChip(){
	//Instruction_Write(0x01, 0x40);
	Instruction_Write(0x01, 0x11); // Conectar 2 Positivo, 1 Negativo en Channel1
	Instruction_Write(0x0A, 0x03); // Agrega inpuits a nodo comun
	Instruction_Write(0x0C, 0x03); // input 3 como Right legh drive
	Instruction_Write(0x13,0x09);  // high frequenciy and res
	Instruction_Write(0x12, 0x04); // Start Clock
	Instruction_Write(0x14, 0x36);	// Shutdown channel 2 ybchannel 3 (ADC y AmP)
	Instruction_Write(0x21, 0x08);  // Decimation Rate r2 
	Instruction_Write(0x22, 0x80); // Decimation Rate ch1
	Instruction_Write(0x27, 0x08); // DRDY activado con channel1 (active_low)
	Instruction_Write(0x2F, 0x10); // Modo Loopback de lectura
	Instruction_Write(0x00, 0x01); // Emp[ezar
}
void PrennderLed(){
	PORTC = 0xFF;
	_delay_ms(500);
	PORTC = 0;
	_delay_ms(500);
}

int main(void)
{
	
	DDRC = 0xFF;
	PORTC = 0xFF;
	_delay_ms(1000);
	PORTC = 0;
	DDRA = 0;
	PORTA = 0xFF;
	sei();
	USART_Init(MYUBRR);
	SPI_INIT_MASTER();
	InicializarChip();
	
	
	read[0] = read[1] = read[2] = 0;
	
	while(1){
		_delay_ms(10);
		while((PINA & (1<<1))) {}
		ReadChip(read);
		SendByte(read[3]);
		SendByte(read[4]);
		SendByte(read[5]);
		SendByte('\n');
	}
	
	
	// no quitar xd
}

