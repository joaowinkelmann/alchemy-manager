#include <stdio.h>
#include <stdlib.h>

#define TOT 9
#define TAB 13

int verifica_validade(int tentativas_restantes, int tabela[TAB][TAB], int symbols[9][4][4], int ini[2]) {
    if (tentativas_restantes == 0) {
        return 0;
    }

    int valid = 0;
    int pos_ini[2];
    pos_ini[0] = ini[0];
    pos_ini[1] = ini[1];
    // printf("pos_ini: %d %d\n", pos_ini[0], pos_ini[1]);

    for (int i = 0; i < TAB; i++) {
        for (int j = 0; j < TAB; j++) {
            if (i == ini[0] && j == ini[1]) {
                for (int k = 0; k < 9; k++) {
                    for (int l = 0; l < 4; l++) {
                        for (int m = 0; m < 4; m++) {
                            if (symbols[k][l][m] == 2) {
                                // printf("pos_ini: %d %d, symbols: %d\n", pos_ini[0], pos_ini[1], k);
                                for (int n = 0; n < 4; n++) {
                                    for (int o = 0; o < 4; o++) {
                                        if (symbols[k][n][o] == 0) {
                                            continue;
                                        }

                                        if (tabela[i + n - l][j + o - m] == -1) {
                                            goto teste;
                                        }

                                        if (symbols[k][n][o] == 3) {
                                            pos_ini[0] = i + n - l;
                                            pos_ini[1] = j + o - m;

                                            // printf("pos_ini: %d %d, symbols: %d\n", pos_ini[0], pos_ini[1], k);
                                        }

                                        if (tabela[i + n - l][j + o - m] == 4 && symbols[k][n][o] == 3) {
                                            valid = 1;
                                        }
                                    }
                                }

                                if (valid == 1) {
                                    printf("k: %d\n", k);
                                    return 1;
                                } else {
                                    // printf("pos_ini: %d %d, k: %d\n", pos_ini[0], pos_ini[1], k);
                                    valid = verifica_validade(tentativas_restantes - 1, tabela, symbols, pos_ini);
                                }

                                if (valid == 1) {
                                    printf("k: %d\n", k);
                                    return 1;
                                }

                                teste:
                                    pos_ini[0] = ini[0];
                                    pos_ini[1] = ini[1];
                            }

                            // if ((i + l) >= TAB || (j + m) >= TAB || tabela[i + l][j + m] == -1) { // Verifica se linha passa por um quadrado bloqueado
                            //     return 0;
                            // }
                        }
                    }
                }
            }
        }
    }

    // printf("pos_ini: %d %d\n", pos_ini[0], pos_ini[1]);


    return 0;
}

int main() {
    int tabela[TAB][TAB];

    int blocked[TOT][2] = {
        {1, 2},
        {1, 6},
        {2, 9},
        {6, 3},
        {7, 4},
        {8, 3},
        {9, 7},
        {9, 8},
        {12, 6}
    };
    
    int center = TAB / 2;

    int dispel[2] = {7, 10};
    int healing[2] = {3, 9};
    int regen[2] = {0, 6};
    int defense[2] = {2, 1};
    int strength[2] = {6, 2};
    int haste[2] = {10, 2};
    int poison[2] = {10, 7};
    int acid[2] = {12, 9};

    int num_potions = 0;

    int potions[8][2] = {
        // {7, 10}, // Dispel
        // {3, 9}, // Healing
        // {0, 6}, // Regen
        // {2, 1}, // Defense
        // {6, 2}, // Strength
        // {10, 2} // Haste
        {10, 7} // Poison
        // {12, 9} // Acid
    };

    for (int i = 0; i < 8; i++)
    {
        if (potions[i][0] != 0 || potions[i][1] != 0)
        {
            num_potions++;
        }
    }
    
    // printf("%d\n", num_potions);
    // return -1;

    int symbols[9][4][4] = {
        // Argosia
        {
            {0, 2, 0, 0},
            {1, 1, 0, 0},
            {1, 1, 0, 0},
            {0, 3, 0, 0}
        },
        // Cinderbloom
        {
            {1, 0, 0, 0},
            {1, 1, 0, 0},
            {2, 0, 3, 0},
            {0, 0, 0, 0}
        },
        // Coronarium
        {
            {0, 2, 0, 0},
            {0, 1, 1, 1},
            {3, 0, 1, 0},
            {0, 1, 0, 0}
        },
        // Howlbane
        {
            {1, 1, 0, 0},
            {1, 1, 0, 0},
            {3, 1, 0, 0},
            {0, 0, 2, 0}
        },
        // Miriagreen
        {
            {0, 1, 1, 0},
            {2, 1, 3, 0},
            {0, 0, 0, 0},
            {0, 0, 0, 0}
        },
        // Paleroot
        {
            {0, 1, 3, 0},
            {1, 0, 0, 0},
            {0, 1, 2, 0},
            {0, 0, 0, 0}
        },
        // Sageleaf
        {
            {0, 0, 2, 0},
            {1, 1, 1, 0},
            {1, 3, 0, 0},
            {0, 0, 0, 0}
        },
        // Thickweed
        {
            {3, 1, 1, 2},
            {0, 0, 0, 1},
            {0, 0, 0, 0},
            {0, 0, 0, 0}
        },
        // Widow's Tear
        {
            {0, 3, 0, 0},
            {0, 1, 0, 0},
            {1, 0, 0, 0},
            {2, 0, 0, 0}
        }
    };

    int ini_block = 0, ini_pot = 0;
    for (int i = 0; i < TAB; i++) {
        for (int j = 0; j < TAB; j++) {
            for (int k = ini_block; k < TOT; k++) {
                if (i == blocked[k][0] && j == blocked[k][1]) {
                    tabela[i][j] = -1;
                    ini_block++;
                    goto jump;
                }
            }

            for (int k = ini_pot; k < num_potions; k++) {
                if (i == potions[k][0] && j == potions[k][1]) {
                    tabela[i][j] = 4;
                    goto jump;
                }
            }

            tabela[i][j] = 0;
            jump: 
        }
    }

    int tentativas_restantes = 5;
    int ini[2] = {center, center};
    int valid = verifica_validade(tentativas_restantes, tabela, symbols, ini);

    if (valid == 1) {
        printf("Valido\n");
    } else {
        printf("Invalido\n");
    }

    for (int i = 0; i < TAB; i++) {
        for (int j = 0; j < TAB; j++) {
            printf("%2d ", tabela[i][j]);
        }
        printf("\n");
    }
}