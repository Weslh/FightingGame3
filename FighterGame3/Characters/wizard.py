import pygame

class Wizard():
    def __init__(self, player, x, y, flip,data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0#0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)

                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale,self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        damage = 0

        #get keypresses
        key = pygame.key.get_pressed()

        #can only perform other actions if not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            #check player 1 controls
            if self.player == 1:
                #movement

                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    #determine which attack type was used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    elif key[pygame.K_t]:
                        self.attack_type = 2
                    self.attack(surface, target, damage)
            #check player 2 controls
            if self.player == 2:
                #movement

                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                #attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    #determine which attack type was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2
                    self.attack(surface, target, damage)

        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        #ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


        #update player position
        self.rect.x += dx
        self.rect.y += dy

    #handle animation updates
    def update(self):
        #check what action player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 100
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation is finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if the player is dead end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #check if attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #check if damage was taken
                if self.action == 5:
                    self.hit = False
                    #if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20


    def attack(self, surface, target, damage):
        if self.attack_cooldown == 0:
            # execute attack
            self.attack_sound.play()
            self.attacking = True

            # Define attack properties based on attack type
            if self.attack_type == 1:
                # Attack type 1 properties
                attack_width = 2 * self.rect.width
                damage = 25
            elif self.attack_type == 2:
                # Attack type 2 properties
                attack_width = 3 * self.rect.width
                damage = 50

            
            # Calculate the x-coordinate of the attacking rectangle based on player direction
            if not self.flip:  # Player facing right
                attacking_x = self.rect.right  # Attack towards the right
            else:  # Player facing left
                attacking_x = self.rect.left - (2 * self.rect.width)  # Attack towards the left
                
            attacking_rect = pygame.Rect(attacking_x, self.rect.y, 2 * self.rect.width, self.rect.height)
            
            if attacking_rect.colliderect(target.rect):
                target.health -= damage
                target.hit = True
                
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def update_action(self, new_action):
        #check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))