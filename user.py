from datetime import datetime
class User():
    def __init__(self,id,state,partner_id = "", nickname = "", gender = "", partner_gender = "", introduce = "", last_action_time ="", previous_id = "", blocks_id = ""):
        self.id = id
        self.state = state
        self.partner_id = partner_id
        self.nickname = nickname
        self.gender = gender
        self.partner_gender = partner_gender
        self.introduce = introduce
        self.last_action_time = last_action_time
        self.previous_id = previous_id
        self.blocks_id = blocks_id

    def set_state(self,current_state):
        self.state = current_state

    def next_state(self):
        self.state = self.state_pipeline[self.state]['next']

    def add_block(self, block_id):
        self.blocks_id = self.blocks_id.append(block_id)

