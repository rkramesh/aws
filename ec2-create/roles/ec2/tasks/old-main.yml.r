#
# Create EC2 Insance Key
- name: Create an EC2 key
  ec2_key:
        name: "{{ ec2.project_name }}-{{ ec2.env }}-{{ ec2.tags }}-key"
        region: "{{ ec2.region }}"
  register: ec2_key
# save Private key 
- name: save private key
  copy: 
    content: "{{ ec2_key.key.private_key }}" 
    dest: "~/.ssh/{{ ec2.project_name }}-{{ ec2.env }}-{{ ec2.tags }}-key.pem"
    mode: 0600
  when: ec2_key.changed 
# Create EC2 Instances
#- name: Create Ec2 Instances
#  ec2:
#    region: "{{ ec2.region }}"
#    key_name: "{{ ec2.project_name }}-{{ ec2.env }}-key"
#    instance_tags: "{{ ec2.tags }}"
#    image: "{{ ec2.image }}"
#    instance_type: "{{ ec2.instance_type }}"
#    instance_profile_name: "{{ec2.role | default('') }}"
#    group: "{{ ec2.sg }}"
#    vpc_subnet_id: "{{ ec2.subnet }}"
#    assign_public_ip: "{{ ec2.public_ip | default('no') }}"
#    private_ip: "{{ ec2.private_ip | default('') }}"
#    wait: true

